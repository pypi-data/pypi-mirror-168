# -*- coding: utf-8 -*-
"""
ElementsWorker methods for entities.
"""

from enum import Enum
from typing import Dict, Optional, Union

from peewee import IntegrityError

from arkindex_worker import logger
from arkindex_worker.cache import CachedElement, CachedEntity, CachedTranscriptionEntity
from arkindex_worker.models import Element, Transcription


class EntityType(Enum):
    """
    Type of an entity.
    """

    Person = "person"
    Location = "location"
    Subject = "subject"
    Organization = "organization"
    Misc = "misc"
    Number = "number"
    Date = "date"


class EntityMixin(object):
    def create_entity(
        self,
        element: Union[Element, CachedElement],
        name: str,
        type: EntityType,
        metas=dict(),
        validated=None,
    ):
        """
        Create an entity on the given corpus.
        If cache support is enabled, a [CachedEntity][arkindex_worker.cache.CachedEntity] will also be created.

        :param element: An element on which the entity will be reported with the [Reporter][arkindex_worker.reporting.Reporter].
           This does not have any effect on the entity itself.
        :param name: Name of the entity.
        :param type: Type of the entity.
        """
        assert element and isinstance(
            element, (Element, CachedElement)
        ), "element shouldn't be null and should be an Element or CachedElement"
        assert name and isinstance(
            name, str
        ), "name shouldn't be null and should be of type str"
        assert type and isinstance(
            type, EntityType
        ), "type shouldn't be null and should be of type EntityType"
        if metas:
            assert isinstance(metas, dict), "metas should be of type dict"
        if validated is not None:
            assert isinstance(validated, bool), "validated should be of type bool"
        if self.is_read_only:
            logger.warning("Cannot create entity as this worker is in read-only mode")
            return

        entity = self.request(
            "CreateEntity",
            body={
                "name": name,
                "type": type.value,
                "metas": metas,
                "validated": validated,
                "corpus": self.corpus_id,
                "worker_version": self.worker_version_id,
            },
        )
        self.report.add_entity(element.id, entity["id"], type.value, name)

        if self.use_cache:
            # Store entity in local cache
            try:
                to_insert = [
                    {
                        "id": entity["id"],
                        "type": type.value,
                        "name": name,
                        "validated": validated if validated is not None else False,
                        "metas": metas,
                        "worker_version_id": self.worker_version_id,
                    }
                ]
                CachedEntity.insert_many(to_insert).execute()
            except IntegrityError as e:
                logger.warning(f"Couldn't save created entity in local cache: {e}")

        return entity["id"]

    def create_transcription_entity(
        self,
        transcription: str,
        entity: str,
        offset: int,
        length: int,
        confidence: Optional[float] = None,
    ) -> Optional[Dict[str, Union[str, int]]]:
        """
        Create a link between an existing entity and an existing transcription.
        If cache support is enabled, a `CachedTranscriptionEntity` will also be created.

        :param transcription: UUID of the existing transcription.
        :param entity: UUID of the existing entity.
        :param offset: Starting position of the entity in the transcription's text,
           as a 0-based index.
        :param length: Length of the entity in the transcription's text.
        :param confidence: Optional confidence score between 0 or 1.
        :returns: A dict as returned by the ``CreateTranscriptionEntity`` API endpoint,
           or None if the worker is in read-only mode.
        """
        assert transcription and isinstance(
            transcription, str
        ), "transcription shouldn't be null and should be of type str"
        assert entity and isinstance(
            entity, str
        ), "entity shouldn't be null and should be of type str"
        assert (
            offset is not None and isinstance(offset, int) and offset >= 0
        ), "offset shouldn't be null and should be a positive integer"
        assert (
            length is not None and isinstance(length, int) and length > 0
        ), "length shouldn't be null and should be a strictly positive integer"
        assert (
            confidence is None or isinstance(confidence, float) and 0 <= confidence <= 1
        ), "confidence should be null or a float in [0..1] range"
        if self.is_read_only:
            logger.warning(
                "Cannot create transcription entity as this worker is in read-only mode"
            )
            return

        body = {
            "entity": entity,
            "length": length,
            "offset": offset,
            "worker_version_id": self.worker_version_id,
        }
        if confidence is not None:
            body["confidence"] = confidence

        transcription_ent = self.request(
            "CreateTranscriptionEntity",
            id=transcription,
            body=body,
        )
        # TODO: Report transcription entity creation

        if self.use_cache:
            # Store transcription entity in local cache
            try:
                CachedTranscriptionEntity.create(
                    transcription=transcription,
                    entity=entity,
                    offset=offset,
                    length=length,
                    worker_version_id=self.worker_version_id,
                    confidence=confidence,
                )
            except IntegrityError as e:
                logger.warning(
                    f"Couldn't save created transcription entity in local cache: {e}"
                )
        return transcription_ent

    def list_transcription_entities(
        self,
        transcription: Transcription,
        worker_version: Optional[Union[str, bool]] = None,
    ):
        """
        List existing entities on a transcription
        This method does not support cache

        :param transcription: The transcription to list entities on.
        :param worker_version: Restrict to entities created by a worker version with this UUID. Set to False to look for manually created transcriptions.
        """
        query_params = {}
        assert transcription and isinstance(
            transcription, Transcription
        ), "transcription shouldn't be null and should be a Transcription"

        if worker_version is not None:
            assert isinstance(
                worker_version, (str, bool)
            ), "worker_version should be of type str or bool"

            if isinstance(worker_version, bool):
                assert (
                    worker_version is False
                ), "if of type bool, worker_version can only be set to False"
            query_params["worker_version"] = worker_version

        return self.api_client.paginate(
            "ListTranscriptionEntities", id=transcription.id, **query_params
        )

    def list_corpus_entities(
        self,
        name: Optional[str] = None,
        parent: Optional[Element] = None,
    ):
        """
        List all entities in the worker's corpus
        This method does not support cache
        :param name: Filter entities by part of their name (case-insensitive)
        :param parent Element: Restrict entities to those linked to all transcriptions of an element and all its descendants. Note that links to metadata are ignored.
        """
        query_params = {}

        if name is not None:
            assert name and isinstance(name, str), "name should be of type str"
            query_params["name"] = name

        if parent is not None:
            assert isinstance(parent, Element), "parent should be of type Element"
            query_params["parent"] = parent.id

        return self.api_client.paginate(
            "ListCorpusEntities", id=self.corpus_id, **query_params
        )
