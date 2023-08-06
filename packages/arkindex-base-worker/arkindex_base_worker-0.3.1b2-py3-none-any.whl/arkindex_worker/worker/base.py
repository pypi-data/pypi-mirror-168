# -*- coding: utf-8 -*-
"""
The base class for all Arkindex workers.
"""

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Optional

import gnupg
import yaml
from apistar.exceptions import ErrorResponse
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from arkindex import ArkindexClient, options_from_env
from arkindex_worker import logger
from arkindex_worker.cache import (
    check_version,
    create_tables,
    create_version_table,
    init_cache_db,
    merge_parents_cache,
    retrieve_parents_cache_path,
)


def _is_500_error(exc: Exception) -> bool:
    """
    Check if an Arkindex API error has a HTTP 5xx error code.
    Used to retry most API calls in [BaseWorker][arkindex_worker.worker.base.BaseWorker].
    :param exc: Exception to check
    """
    if not isinstance(exc, ErrorResponse):
        return False

    return 500 <= exc.status_code < 600


class ModelNotFoundError(Exception):
    """
    Exception raised when the path towards the model is invalid
    """


class BaseWorker(object):
    """
    Base class for Arkindex workers.
    """

    def __init__(
        self,
        description: Optional[str] = "Arkindex Base Worker",
        support_cache: Optional[bool] = False,
    ):
        """
        Initialize the worker.

        :param description: Description shown in the ``worker-...`` command line tool.
        :param support_cache: Whether or not this worker supports the cache database.
           Override the constructor and set this parameter to start using the cache database.
        """

        self.parser = argparse.ArgumentParser(description=description)
        self.parser.add_argument(
            "-c",
            "--config",
            help="Alternative configuration file when running without a Worker Version ID",
            type=open,
        )
        self.parser.add_argument(
            "-d",
            "--database",
            help="Alternative SQLite database to use for worker caching",
            type=str,
            default=None,
        )
        self.parser.add_argument(
            "-v",
            "--verbose",
            "--debug",
            help="Display more information on events and errors",
            action="store_true",
            default=False,
        )
        self.parser.add_argument(
            "--dev",
            help=(
                "Run worker in developer mode. "
                "Worker will be in read-only state even if a worker_version is supplied. "
            ),
            action="store_true",
            default=False,
        )
        # To load models locally
        self.parser.add_argument(
            "--model-dir",
            help=("The path to a local model's directory (development only)."),
            type=Path,
        )

        # Call potential extra arguments
        self.add_arguments()

        # Setup workdir either in Ponos environment or on host's home
        if os.environ.get("PONOS_DATA"):
            self.work_dir = os.path.join(os.environ["PONOS_DATA"], "current")
        else:
            # We use the official XDG convention to store file for developers
            # https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
            xdg_data_home = os.environ.get(
                "XDG_DATA_HOME", os.path.expanduser("~/.local/share")
            )
            self.work_dir = os.path.join(xdg_data_home, "arkindex")
            os.makedirs(self.work_dir, exist_ok=True)

        # Store task ID. This is only available when running in production
        # through a ponos agent
        self.task_id = os.environ.get("PONOS_TASK")

        self.worker_version_id = os.environ.get("WORKER_VERSION_ID")
        if not self.worker_version_id:
            logger.warning(
                "Missing WORKER_VERSION_ID environment variable, worker is in read-only mode"
            )
        self.worker_run_id = os.environ.get("ARKINDEX_WORKER_RUN_ID")
        if not self.worker_run_id:
            logger.warning(
                "Missing ARKINDEX_WORKER_RUN_ID environment variable, worker is in read-only mode"
            )

        logger.info(f"Worker will use {self.work_dir} as working directory")

        self.process_information = None
        # corpus_id will be updated in configure() using the worker_run's corpus
        # or in configure_for_developers() from the environment
        self.corpus_id = None
        self.user_configuration = {}
        self.model_configuration = {}
        self.support_cache = support_cache
        # use_cache will be updated in configure() if the cache is supported and if there
        # is at least one available sqlite database either given or in the parent tasks
        self.use_cache = False

        # Define API Client
        self.setup_api_client()

    @property
    def is_read_only(self) -> bool:
        """
        Whether or not the worker can publish data.

        :returns: False when dev mode is enabled with the ``--dev`` CLI argument,
            when no worker version ID is provided or when no worker run ID is provided
        """
        return (
            self.args.dev
            or self.worker_version_id is None
            or self.worker_run_id is None
        )

    def setup_api_client(self):
        """
        Create an ArkindexClient to make API requests towards Arkindex instances.
        """
        # Build Arkindex API client from environment variables
        self.api_client = ArkindexClient(**options_from_env())
        logger.debug(f"Setup Arkindex API client on {self.api_client.document.url}")

    def configure_for_developers(self):
        """
        Setup the necessary configuration needed when working in `read_only` mode.
        This is the method called when running a worker locally.
        """
        assert self.is_read_only
        # Setup logging level if verbose or if ARKINDEX_DEBUG is set to true
        if self.args.verbose or os.environ.get("ARKINDEX_DEBUG"):
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug output enabled")

        if self.args.config:
            # Load config from YAML file
            self.config = yaml.safe_load(self.args.config)
            self.worker_details = {"name": "Local worker"}
            required_secrets = self.config.get("secrets", [])
            logger.info(
                f"Running with local configuration from {self.args.config.name}"
            )
        else:
            self.config = {}
            self.worker_details = {}
            required_secrets = []
            logger.warning("Running without any extra configuration")

        # Define corpus_id from environment
        self.corpus_id = os.environ.get("ARKINDEX_CORPUS_ID")

        # Load all required secrets
        self.secrets = {name: self.load_secret(name) for name in required_secrets}

    def configure(self):
        """
        Setup the necessary configuration needed using CLI args and environment variables.
        This is the method called when running a worker on Arkindex.
        """
        assert not self.is_read_only
        # Setup logging level if verbose or if ARKINDEX_DEBUG is set to true
        if self.args.verbose or os.environ.get("ARKINDEX_DEBUG"):
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug output enabled")

        # Load worker run information
        worker_run = self.request("RetrieveWorkerRun", id=self.worker_run_id)

        # Load process information
        self.process_information = worker_run["process"]

        # Load corpus id
        self.corpus_id = worker_run["process"]["corpus"]

        # Load worker version information
        worker_version = worker_run["worker_version"]
        self.worker_details = worker_version["worker"]
        logger.info(
            f"Loaded worker {self.worker_details['name']} revision {worker_version['revision']['hash'][0:7]} from API"
        )

        # Retrieve initial configuration from API
        self.config = worker_version["configuration"].get("configuration")
        if "user_configuration" in worker_version["configuration"]:
            # Add default values (if set) to user_configuration
            for key, value in worker_version["configuration"][
                "user_configuration"
            ].items():
                if "default" in value:
                    self.user_configuration[key] = value["default"]

        # Load all required secrets
        required_secrets = worker_version["configuration"].get("secrets", [])
        self.secrets = {name: self.load_secret(name) for name in required_secrets}

        # Load worker run configuration when available
        worker_configuration = worker_run.get("configuration")
        if worker_configuration and worker_configuration.get("configuration"):
            logger.info("Loaded user configuration from WorkerRun")
            self.user_configuration.update(worker_configuration.get("configuration"))

        # Load model version configuration when available
        model_version = worker_run.get("model_version")
        if model_version and model_version.get("configuration"):
            logger.info("Loaded model version configuration from WorkerRun")
            self.model_configuration.update(model_version.get("configuration"))

        # if debug mode is set to true activate debug mode in logger
        if self.user_configuration.get("debug"):
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug output enabled")

    def configure_cache(self):
        """
        Setup the necessary attribute when using the cache system of `Base-Worker`.
        """
        paths = None
        if self.support_cache and self.args.database is not None:
            self.use_cache = True
        elif self.support_cache and self.task_id:
            task = self.request("RetrieveTaskFromAgent", id=self.task_id)
            paths = retrieve_parents_cache_path(
                task["parents"],
                data_dir=os.environ.get("PONOS_DATA", "/data"),
                chunk=os.environ.get("ARKINDEX_TASK_CHUNK"),
            )
            self.use_cache = len(paths) > 0

        if self.use_cache:
            if self.args.database is not None:
                assert os.path.isfile(
                    self.args.database
                ), f"Database in {self.args.database} does not exist"
                self.cache_path = self.args.database
            else:
                cache_dir = os.path.join(
                    os.environ.get("PONOS_DATA", "/data"), self.task_id
                )
                assert os.path.isdir(cache_dir), f"Missing task cache in {cache_dir}"
                self.cache_path = os.path.join(cache_dir, "db.sqlite")

            init_cache_db(self.cache_path)

            if self.args.database is not None:
                check_version(self.cache_path)
            else:
                create_version_table()

            create_tables()

            # Merging parents caches (if there are any) in the current task local cache, unless the database got overridden
            if self.args.database is None and paths is not None:
                merge_parents_cache(paths, self.cache_path)
        else:
            logger.debug("Cache is disabled")

    def load_secret(self, name: str):
        """
        Load a Ponos secret by name.

        :param name: Name of the Ponos secret.
        :raises Exception: When the secret cannot be loaded from the API nor the local secrets directory.
        """
        secret = None

        # Load from the backend
        try:
            resp = self.request("RetrieveSecret", name=name)
            secret = resp["content"]
            logging.info(f"Loaded API secret {name}")
        except ErrorResponse as e:
            logger.warning(f"Secret {name} not available: {e.content}")

        # Load from local developer storage
        base_dir = Path(os.environ.get("XDG_CONFIG_HOME") or "~/.config").expanduser()
        path = base_dir / "arkindex" / "secrets" / name
        if path.exists():
            logging.debug(f"Loading local secret from {path}")

            try:
                gpg = gnupg.GPG()
                decrypted = gpg.decrypt_file(open(path, "rb"))
                assert (
                    decrypted.ok
                ), f"GPG error: {decrypted.status} - {decrypted.stderr}"
                secret = decrypted.data.decode("utf-8")
                logging.info(f"Loaded local secret {name}")
            except Exception as e:
                logger.error(f"Local secret {name} is not available as {path}: {e}")

        if secret is None:
            raise Exception(f"Secret {name} is not available on the API nor locally")

        # Parse secret payload, according to its extension
        _, ext = os.path.splitext(os.path.basename(name))
        try:
            ext = ext.lower()
            if ext == ".json":
                return json.loads(secret)
            elif ext in (".yaml", ".yml"):
                return yaml.safe_load(secret)
        except Exception as e:
            logger.error(f"Failed to parse secret {name}: {e}")

        # By default give raw secret payload
        return secret

    def find_model_directory(self) -> Path:
        """
        Find the local path to the model. This supports two modes:
        - the worker runs in ponos, the model is available at `/data/current`
        - the worker runs locally, the developer may specify it using either
           - the `model_dir` configuration parameter
           - the `--model-dir` CLI parameter

        :return: Path to the model on disk
        """
        if self.task_id:
            # When running in production with ponos, the agent
            # downloads the model and set it in the current task work dir
            return Path(self.work_dir)
        else:
            model_dir = self.config.get("model_dir", self.args.model_dir)
            if model_dir is None:
                raise ModelNotFoundError(
                    "No path to the model was provided. "
                    "Please provide model_dir either through configuration "
                    "or as CLI argument."
                )
            model_dir = Path(model_dir)
            if not model_dir.exists():
                raise ModelNotFoundError(
                    f"The path {model_dir} does not link to any directory"
                )
            return model_dir

    @retry(
        retry=retry_if_exception(_is_500_error),
        wait=wait_exponential(multiplier=2, min=3),
        reraise=True,
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.INFO),
    )
    def request(self, *args, **kwargs):
        """
        Wrapper around the ``ArkindexClient.request`` method.

        The API call will be retried up to 5 times in case of HTTP 5xx errors,
        with an exponential sleep time of 3, 4, 8 and 16 seconds between calls.
        If the 5th call still causes an HTTP 5xx error, the exception is re-raised
        and the caller should catch it.

        Log messages are displayed when an HTTP 5xx error occurs, before waiting for the next call.
        """
        return self.api_client.request(*args, **kwargs)

    def add_arguments(self):
        """Override this method to add ``argparse`` arguments to this worker"""

    def run(self):
        """Override this method to implement your own process"""
