# -*- coding: utf-8 -*-
"""
BaseWorker methods for training.
"""

import hashlib
import os
import tarfile
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import NewType, Optional, Tuple

import requests
import zstandard as zstd
from apistar.exceptions import ErrorResponse

from arkindex_worker import logger

CHUNK_SIZE = 1024

DirPath = NewType("DirPath", str)
"""Path to a directory"""

Hash = NewType("Hash", str)
"""MD5 Hash"""

FileSize = NewType("FileSize", int)
"""File size"""


@contextmanager
def create_archive(path: DirPath) -> Tuple[Path, Hash, FileSize, Hash]:
    """
    Create a tar archive from the files at the given location then compress it to a zst archive.

    Yield its location, its hash, its size and its content's hash.

    :param path: Create a compressed tar archive from the files
    :returns: The location of the created archive, its hash, its size and its content's hash
    """
    assert path.is_dir(), "create_archive needs a directory"

    compressor = zstd.ZstdCompressor(level=3)
    content_hasher = hashlib.md5()
    archive_hasher = hashlib.md5()

    # Remove extension from the model filename
    _, path_to_tar_archive = tempfile.mkstemp(prefix="teklia-", suffix=".tar")

    # Create an uncompressed tar archive with all the needed files
    # Files hierarchy ifs kept in the archive.
    file_list = []
    with tarfile.open(path_to_tar_archive, "w") as tar:
        for p in path.glob("**/*"):
            x = p.relative_to(path)
            tar.add(p, arcname=x, recursive=False)
            file_list.append(p)

    # Sort by path
    file_list.sort()
    # Compute hash of the files
    for file_path in file_list:
        with open(file_path, "rb") as file_data:
            for chunk in iter(lambda: file_data.read(CHUNK_SIZE), b""):
                content_hasher.update(chunk)

    _, path_to_zst_archive = tempfile.mkstemp(prefix="teklia-", suffix=".tar.zst")

    # Compress the archive
    with open(path_to_zst_archive, "wb") as archive_file:
        with open(path_to_tar_archive, "rb") as model_data:
            for model_chunk in iter(lambda: model_data.read(CHUNK_SIZE), b""):
                compressed_chunk = compressor.compress(model_chunk)
                archive_hasher.update(compressed_chunk)
                archive_file.write(compressed_chunk)

    # Remove the tar archive
    os.remove(path_to_tar_archive)

    # Get content hash, archive size and hash
    hash = content_hasher.hexdigest()
    size = os.path.getsize(path_to_zst_archive)
    archive_hash = archive_hasher.hexdigest()

    yield path_to_zst_archive, hash, size, archive_hash

    # Remove the zstd archive
    os.remove(path_to_zst_archive)


class TrainingMixin(object):
    def publish_model_version(
        self,
        model_path: DirPath,
        model_id: str,
        tag: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """
        This method creates a model archive and its associated hash,
        to create a unique version that will be stored on a bucket and published on Arkindex.

        :param model_path: Path to the directory containing the model version's files.
        :param model_id: ID of the model
        :param tag:
        :param description:
        """

        if self.is_read_only:
            logger.warning(
                "Cannot publish a new model version as this worker is in read-only mode"
            )
            return

        # Create the zst archive, get its hash and size
        with create_archive(path=model_path) as (
            path_to_archive,
            hash,
            size,
            archive_hash,
        ):
            # Create a new model version with hash and size
            model_version_details = self.create_model_version(
                model_id=model_id,
                hash=hash,
                size=size,
                archive_hash=archive_hash,
                tag=tag,
                description=description,
            )
            if model_version_details is None:
                return
            self.upload_to_s3(
                archive_path=path_to_archive,
                model_version_details=model_version_details,
            )

        # Update the model version with state, configuration parsed, tag, description (defaults to name of the worker)
        self.update_model_version(
            model_version_details=model_version_details,
        )

    def create_model_version(
        self,
        model_id: str,
        hash: str,
        size: int,
        archive_hash: str,
        tag: str,
        description: str,
    ) -> dict:
        """
        Create a new version of the specified model with the given information (hashes and size).
        If a version matching the information already exist, there are two cases:
        - The version is in `Created` state: this version's details is used
        - The version is in `Available` state: you cannot create twice the same version, an error is raised
        """
        if self.is_read_only:
            logger.warning(
                "Cannot create a new model version as this worker is in read-only mode"
            )
            return

        # Create a new model version with hash and size
        try:
            payload = {"hash": hash, "size": size, "archive_hash": archive_hash}
            if tag:
                payload["tag"] = tag
            if description:
                payload["description"] = description
            model_version_details = self.request(
                "CreateModelVersion",
                id=model_id,
                body=payload,
            )
            logger.info(
                f"Model version ({model_version_details['id']}) was created successfully"
            )
        except ErrorResponse as e:
            model_version_details = (
                e.content.get("hash") if hasattr(e, "content") else None
            )
            if e.status_code >= 500 or model_version_details is None:
                logger.error(f"Failed to create model version: {e.content}")
                raise e
            # If the existing model is in Created state, this model is returned as a dict.
            # Else an error in a list is returned.
            if isinstance(model_version_details, (list, tuple)):
                logger.error(model_version_details[0])
                return

            logger.info(
                f"Model version ({model_version_details['id']}) has the same hash, using this one instead of creating one"
            )

        return model_version_details

    def upload_to_s3(self, archive_path: str, model_version_details: dict) -> None:
        """
        Upload the archive of the model's files to an Amazon s3 compatible storage
        """
        if self.is_read_only:
            logger.warning(
                "Cannot upload this archive as this worker is in read-only mode"
            )
            return

        s3_put_url = model_version_details.get("s3_put_url")
        logger.info("Uploading to s3...")
        # Upload the archive on s3
        with open(archive_path, "rb") as archive:
            r = requests.put(
                url=s3_put_url,
                data=archive,
                headers={"Content-Type": "application/zstd"},
            )
        r.raise_for_status()

    def update_model_version(
        self,
        model_version_details: dict,
        configuration: dict = {},
    ) -> None:
        """
        Update the specified model version to the state `Available` and use the given information"
        """
        if self.is_read_only:
            logger.warning(
                "Cannot update this model version as this worker is in read-only mode"
            )
            return

        model_version_id = model_version_details.get("id")
        logger.info(f"Updating model version ({model_version_id})")
        try:
            self.request(
                "UpdateModelVersion",
                id=model_version_id,
                body={
                    "state": "available",
                    "description": model_version_details.get("description"),
                    "configuration": configuration,
                    "tag": model_version_details.get("tag"),
                },
            )
            logger.info(f"Model version ({model_version_id}) was successfully updated")
        except ErrorResponse as e:
            logger.error(f"Failed to update model version: {e.content}")
