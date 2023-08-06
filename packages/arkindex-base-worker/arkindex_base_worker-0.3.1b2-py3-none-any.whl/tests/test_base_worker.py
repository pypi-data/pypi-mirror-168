# -*- coding: utf-8 -*-
import json
import logging
import os
import sys
from pathlib import Path

import gnupg
import pytest

from arkindex.mock import MockApiClient
from arkindex_worker import logger
from arkindex_worker.worker import BaseWorker
from arkindex_worker.worker.base import ModelNotFoundError


def test_init_default_local_share(monkeypatch):
    worker = BaseWorker()

    assert worker.work_dir == os.path.expanduser("~/.local/share/arkindex")
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"


def test_init_default_xdg_data_home(monkeypatch):
    path = str(Path(__file__).absolute().parent)
    monkeypatch.setenv("XDG_DATA_HOME", path)
    worker = BaseWorker()

    assert worker.work_dir == f"{path}/arkindex"
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"


def test_init_with_local_cache(monkeypatch):
    worker = BaseWorker(support_cache=True)

    assert worker.work_dir == os.path.expanduser("~/.local/share/arkindex")
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"
    assert worker.support_cache is True


def test_init_var_ponos_data_given(monkeypatch):
    path = str(Path(__file__).absolute().parent)
    monkeypatch.setenv("PONOS_DATA", path)
    worker = BaseWorker()

    assert worker.work_dir == f"{path}/current"
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"


def test_init_var_worker_version_id_missing(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["worker"])
    monkeypatch.delenv("WORKER_VERSION_ID")
    monkeypatch.delenv("ARKINDEX_WORKER_RUN_ID")
    worker = BaseWorker()
    worker.args = worker.parser.parse_args()
    worker.configure_for_developers()
    assert worker.worker_version_id is None
    assert worker.is_read_only is True
    assert worker.config == {}  # default empty case


def test_init_var_worker_run_id_missing(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["worker"])
    monkeypatch.delenv("ARKINDEX_WORKER_RUN_ID")
    worker = BaseWorker()
    worker.args = worker.parser.parse_args()
    worker.configure_for_developers()
    assert worker.worker_run_id is None
    assert worker.is_read_only is True
    assert worker.config == {}  # default empty case


def test_init_var_worker_local_file(monkeypatch, tmp_path):
    # Build a dummy yaml config file
    config = tmp_path / "config.yml"
    config.write_text("---\nlocalKey: abcdef123")

    monkeypatch.setattr(sys, "argv", ["worker", "-c", str(config)])
    monkeypatch.delenv("WORKER_VERSION_ID")
    monkeypatch.delenv("ARKINDEX_WORKER_RUN_ID")
    worker = BaseWorker()
    worker.args = worker.parser.parse_args()
    worker.configure_for_developers()
    assert worker.worker_version_id is None
    assert worker.is_read_only is True
    assert worker.config == {"localKey": "abcdef123"}  # Use a local file for devs

    config.unlink()


def test_cli_default(mocker, mock_worker_run_api):
    worker = BaseWorker()
    assert logger.level == logging.NOTSET

    mocker.patch.object(sys, "argv", ["worker"])
    worker.args = worker.parser.parse_args()
    assert worker.is_read_only is False
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"
    assert worker.worker_run_id == "56785678-5678-5678-5678-567856785678"

    worker.configure()
    assert not worker.args.verbose
    assert logger.level == logging.NOTSET
    assert worker.api_client
    assert worker.config == {"someKey": "someValue"}  # from API

    logger.setLevel(logging.NOTSET)


def test_cli_arg_verbose_given(mocker, mock_worker_run_api):
    worker = BaseWorker()
    assert logger.level == logging.NOTSET

    mocker.patch.object(sys, "argv", ["worker", "-v"])
    worker.args = worker.parser.parse_args()
    assert worker.is_read_only is False
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"
    assert worker.worker_run_id == "56785678-5678-5678-5678-567856785678"

    worker.configure()
    assert worker.args.verbose
    assert logger.level == logging.DEBUG
    assert worker.api_client
    assert worker.config == {"someKey": "someValue"}  # from API

    logger.setLevel(logging.NOTSET)


def test_cli_envvar_debug_given(mocker, monkeypatch, mock_worker_run_api):
    worker = BaseWorker()

    assert logger.level == logging.NOTSET
    mocker.patch.object(sys, "argv", ["worker"])
    monkeypatch.setenv("ARKINDEX_DEBUG", "True")
    worker.args = worker.parser.parse_args()
    assert worker.is_read_only is False
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"
    assert worker.worker_run_id == "56785678-5678-5678-5678-567856785678"

    worker.configure()
    assert logger.level == logging.DEBUG
    assert worker.api_client
    assert worker.config == {"someKey": "someValue"}  # from API

    logger.setLevel(logging.NOTSET)


def test_configure_dev_mode(mocker, monkeypatch):
    """
    Configuring a worker in developer mode avoid retrieving process information
    """
    worker = BaseWorker()
    mocker.patch.object(sys, "argv", ["worker", "--dev"])
    worker.args = worker.parser.parse_args()
    worker.configure_for_developers()

    assert worker.args.dev is True
    assert worker.process_information is None
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"
    assert worker.worker_run_id == "56785678-5678-5678-5678-567856785678"
    assert worker.is_read_only is True
    assert worker.user_configuration == {}


def test_configure_worker_run(mocker, monkeypatch, responses):
    worker = BaseWorker()
    mocker.patch.object(sys, "argv", ["worker"])
    user_configuration = {
        "id": "bbbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        "name": "BBB",
        "configuration": {"a": "b"},
    }
    payload = {
        "id": "56785678-5678-5678-5678-567856785678",
        "parents": [],
        "worker_version_id": "12341234-1234-1234-1234-123412341234",
        "model_version_id": None,
        "dataimport_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
        "worker": {
            "id": "deadbeef-1234-5678-1234-worker",
            "name": "Fake worker",
            "slug": "fake_worker",
            "type": "classifier",
        },
        "configuration_id": user_configuration["id"],
        "worker_version": {
            "id": "12341234-1234-1234-1234-123412341234",
            "worker": {
                "id": "deadbeef-1234-5678-1234-worker",
                "name": "Fake worker",
                "slug": "fake_worker",
                "type": "classifier",
            },
            "revision": {"hash": "deadbeef1234"},
            "configuration": {"configuration": {}},
        },
        "configuration": user_configuration,
        "model_version": None,
        "process": {
            "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
            "corpus": "11111111-1111-1111-1111-111111111111",
        },
    }

    responses.add(
        responses.GET,
        "http://testserver/api/v1/imports/workers/56785678-5678-5678-5678-567856785678/",
        status=200,
        body=json.dumps(payload),
        content_type="application/json",
    )
    worker.args = worker.parser.parse_args()
    assert worker.is_read_only is False
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"
    assert worker.worker_run_id == "56785678-5678-5678-5678-567856785678"

    worker.configure()

    assert worker.user_configuration == {"a": "b"}


def test_configure_user_configuration_defaults(
    mocker,
    monkeypatch,
    responses,
):
    worker = BaseWorker()
    mocker.patch.object(sys, "argv")
    worker.args = worker.parser.parse_args()

    payload = {
        "id": "56785678-5678-5678-5678-567856785678",
        "parents": [],
        "worker_version_id": "12341234-1234-1234-1234-123412341234",
        "model_version_id": None,
        "dataimport_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
        "worker": {
            "id": "deadbeef-1234-5678-1234-worker",
            "name": "Fake worker",
            "slug": "fake_worker",
            "type": "classifier",
        },
        "configuration_id": "af0daaf4-983e-4703-a7ed-a10f146d6684",
        "worker_version": {
            "id": "12341234-1234-1234-1234-123412341234",
            "worker": {
                "id": "deadbeef-1234-5678-1234-worker",
                "name": "Fake worker",
                "slug": "fake_worker",
                "type": "classifier",
            },
            "revision": {"hash": "deadbeef1234"},
            "configuration": {
                "configuration": {"param_1": "/some/path/file.pth", "param_2": 12},
                "user_configuration": {
                    "integer_parameter": {
                        "type": "int",
                        "title": "Lambda",
                        "default": 0,
                        "required": False,
                    }
                },
            },
        },
        "configuration": {
            "id": "af0daaf4-983e-4703-a7ed-a10f146d6684",
            "name": "my-userconfig",
            "configuration": {
                "param_3": "Animula vagula blandula",
                "param_5": True,
            },
        },
        "model_version": None,
        "process": {
            "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
            "corpus": "11111111-1111-1111-1111-111111111111",
        },
    }
    responses.add(
        responses.GET,
        "http://testserver/api/v1/imports/workers/56785678-5678-5678-5678-567856785678/",
        status=200,
        body=json.dumps(payload),
        content_type="application/json",
    )

    worker.configure()

    assert worker.config == {"param_1": "/some/path/file.pth", "param_2": 12}
    assert worker.user_configuration == {
        "integer_parameter": 0,
        "param_3": "Animula vagula blandula",
        "param_5": True,
    }


@pytest.mark.parametrize("debug", (True, False))
def test_configure_user_config_debug(mocker, monkeypatch, responses, debug):
    worker = BaseWorker()
    mocker.patch.object(sys, "argv", ["worker"])
    assert logger.level == logging.NOTSET
    payload = {
        "id": "56785678-5678-5678-5678-567856785678",
        "parents": [],
        "worker_version_id": "12341234-1234-1234-1234-123412341234",
        "model_version_id": None,
        "dataimport_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
        "worker": {
            "id": "deadbeef-1234-5678-1234-worker",
            "name": "Fake worker",
            "slug": "fake_worker",
            "type": "classifier",
        },
        "configuration_id": "af0daaf4-983e-4703-a7ed-a10f146d6684",
        "worker_version": {
            "id": "12341234-1234-1234-1234-123412341234",
            "worker": {
                "id": "deadbeef-1234-5678-1234-worker",
                "name": "Fake worker",
                "slug": "fake_worker",
                "type": "classifier",
            },
            "revision": {"hash": "deadbeef1234"},
            "configuration": {"configuration": {}},
        },
        "model_version": None,
        "configuration": {
            "id": "af0daaf4-983e-4703-a7ed-a10f146d6684",
            "name": "BBB",
            "configuration": {"debug": debug},
        },
        "process": {
            "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
            "corpus": "11111111-1111-1111-1111-111111111111",
        },
    }
    responses.add(
        responses.GET,
        "http://testserver/api/v1/imports/workers/56785678-5678-5678-5678-567856785678/",
        status=200,
        body=json.dumps(payload),
        content_type="application/json",
    )
    worker.args = worker.parser.parse_args()
    worker.configure()

    assert worker.user_configuration == {"debug": debug}
    expected_log_level = logging.DEBUG if debug else logging.NOTSET
    assert logger.level == expected_log_level
    logger.setLevel(logging.NOTSET)


def test_configure_worker_run_missing_conf(mocker, monkeypatch, responses):
    worker = BaseWorker()
    mocker.patch.object(sys, "argv", ["worker"])

    payload = {
        "id": "56785678-5678-5678-5678-567856785678",
        "parents": [],
        "worker_version_id": "12341234-1234-1234-1234-123412341234",
        "model_version_id": None,
        "dataimport_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
        "worker": {
            "id": "deadbeef-1234-5678-1234-worker",
            "name": "Fake worker",
            "slug": "fake_worker",
            "type": "classifier",
        },
        "configuration_id": "bbbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        "worker_version": {
            "id": "12341234-1234-1234-1234-123412341234",
            "worker": {
                "id": "deadbeef-1234-5678-1234-worker",
                "name": "Fake worker",
                "slug": "fake_worker",
                "type": "classifier",
            },
            "revision": {"hash": "deadbeef1234"},
            "configuration": {"configuration": {}},
        },
        "model_version": None,
        "configuration": {"id": "bbbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", "name": "BBB"},
        "process": {
            "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
            "corpus": "11111111-1111-1111-1111-111111111111",
        },
    }
    responses.add(
        responses.GET,
        "http://testserver/api/v1/imports/workers/56785678-5678-5678-5678-567856785678/",
        status=200,
        body=json.dumps(payload),
        content_type="application/json",
    )
    worker.args = worker.parser.parse_args()
    worker.configure()

    assert worker.user_configuration == {}


def test_configure_worker_run_no_worker_run_conf(mocker, monkeypatch, responses):
    """
    No configuration is provided but should not crash
    """
    worker = BaseWorker()
    mocker.patch.object(sys, "argv", ["worker"])

    payload = {
        "id": "56785678-5678-5678-5678-567856785678",
        "parents": [],
        "worker_version_id": "12341234-1234-1234-1234-123412341234",
        "model_version_id": None,
        "dataimport_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
        "worker": {
            "id": "deadbeef-1234-5678-1234-worker",
            "name": "Fake worker",
            "slug": "fake_worker",
            "type": "classifier",
        },
        "configuration_id": None,
        "worker_version": {
            "id": "12341234-1234-1234-1234-123412341234",
            "worker": {
                "id": "deadbeef-1234-5678-1234-worker",
                "name": "Fake worker",
                "slug": "fake_worker",
                "type": "classifier",
            },
            "revision": {"hash": "deadbeef1234"},
            "configuration": {},
        },
        "model_version": None,
        "configuration": None,
        "process": {
            "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
            "corpus": "11111111-1111-1111-1111-111111111111",
        },
    }
    responses.add(
        responses.GET,
        "http://testserver/api/v1/imports/workers/56785678-5678-5678-5678-567856785678/",
        status=200,
        body=json.dumps(payload),
        content_type="application/json",
    )
    worker.args = worker.parser.parse_args()
    worker.configure()

    assert worker.user_configuration == {}


def test_configure_load_model_configuration(mocker, monkeypatch, responses):
    worker = BaseWorker()
    mocker.patch.object(sys, "argv", ["worker"])
    payload = {
        "id": "56785678-5678-5678-5678-567856785678",
        "parents": [],
        "worker_version_id": "12341234-1234-1234-1234-123412341234",
        "model_version_id": "12341234-1234-1234-1234-123412341234",
        "dataimport_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
        "worker": {
            "id": "deadbeef-1234-5678-1234-worker",
            "name": "Fake worker",
            "slug": "fake_worker",
            "type": "classifier",
        },
        "configuration_id": None,
        "worker_version": {
            "id": "12341234-1234-1234-1234-123412341234",
            "worker": {
                "id": "deadbeef-1234-5678-1234-worker",
                "name": "Fake worker",
                "slug": "fake_worker",
                "type": "classifier",
            },
            "revision": {"hash": "deadbeef1234"},
            "configuration": {"configuration": {}},
        },
        "configuration": None,
        "model_version": {
            "id": "12341234-1234-1234-1234-123412341234",
            "name": "Model version 1337",
            "configuration": {
                "param1": "value1",
                "param2": 2,
                "param3": None,
            },
        },
        "process": {
            "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeffff",
            "corpus": "11111111-1111-1111-1111-111111111111",
        },
    }

    responses.add(
        responses.GET,
        "http://testserver/api/v1/imports/workers/56785678-5678-5678-5678-567856785678/",
        status=200,
        body=json.dumps(payload),
        content_type="application/json",
    )
    worker.args = worker.parser.parse_args()
    assert worker.is_read_only is False
    assert worker.worker_version_id == "12341234-1234-1234-1234-123412341234"
    assert worker.worker_run_id == "56785678-5678-5678-5678-567856785678"
    assert worker.model_configuration == {}

    worker.configure()

    assert worker.model_configuration == {
        "param1": "value1",
        "param2": 2,
        "param3": None,
    }


def test_load_missing_secret():
    worker = BaseWorker()
    worker.api_client = MockApiClient()

    with pytest.raises(
        Exception, match="Secret missing/secret is not available on the API nor locally"
    ):
        worker.load_secret("missing/secret")


def test_load_remote_secret():
    worker = BaseWorker()
    worker.api_client = MockApiClient()
    worker.api_client.add_response(
        "RetrieveSecret",
        name="testRemote",
        response={"content": "this is a secret value !"},
    )

    assert worker.load_secret("testRemote") == "this is a secret value !"

    # The one mocked call has been used
    assert len(worker.api_client.history) == 1
    assert len(worker.api_client.responses) == 0


def test_load_json_secret():
    worker = BaseWorker()
    worker.api_client = MockApiClient()
    worker.api_client.add_response(
        "RetrieveSecret",
        name="path/to/file.json",
        response={"content": '{"key": "value", "number": 42}'},
    )

    assert worker.load_secret("path/to/file.json") == {
        "key": "value",
        "number": 42,
    }

    # The one mocked call has been used
    assert len(worker.api_client.history) == 1
    assert len(worker.api_client.responses) == 0


def test_load_yaml_secret():
    worker = BaseWorker()
    worker.api_client = MockApiClient()
    worker.api_client.add_response(
        "RetrieveSecret",
        name="path/to/file.yaml",
        response={
            "content": """---
somekey: value
aList:
  - A
  - B
  - C
struct:
 level:
   X
"""
        },
    )

    assert worker.load_secret("path/to/file.yaml") == {
        "aList": ["A", "B", "C"],
        "somekey": "value",
        "struct": {"level": "X"},
    }

    # The one mocked call has been used
    assert len(worker.api_client.history) == 1
    assert len(worker.api_client.responses) == 0


def test_load_local_secret(monkeypatch, tmpdir):
    # Setup arkindex config dir in a temp directory
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmpdir))

    # Write a dummy secret
    secrets_dir = tmpdir / "arkindex" / "secrets"
    os.makedirs(secrets_dir)
    secret = secrets_dir / "testLocal"
    secret.write_text("this is a local secret value", encoding="utf-8")

    # Mock GPG decryption
    class GpgDecrypt(object):
        def __init__(self, fd):
            self.ok = True
            self.data = fd.read()

    monkeypatch.setattr(gnupg.GPG, "decrypt_file", lambda gpg, f: GpgDecrypt(f))

    worker = BaseWorker()
    worker.api_client = MockApiClient()

    assert worker.load_secret("testLocal") == "this is a local secret value"

    # The remote api is checked first
    assert len(worker.api_client.history) == 1
    assert worker.api_client.history[0].operation == "RetrieveSecret"


def test_find_model_directory_ponos(monkeypatch):
    monkeypatch.setenv("PONOS_TASK", "my_task")
    monkeypatch.setenv("PONOS_DATA", "/data")
    worker = BaseWorker()
    assert worker.find_model_directory() == Path("/data/current")


def test_find_model_directory_from_cli(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["worker", "--model-dir", "models"])
    monkeypatch.setattr("pathlib.Path.exists", lambda x: True)
    worker = BaseWorker()
    worker.args = worker.parser.parse_args()
    worker.config = {}
    assert worker.find_model_directory() == Path("models")


def test_find_model_directory_from_config(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["worker"])
    monkeypatch.setattr("pathlib.Path.exists", lambda x: True)
    worker = BaseWorker()
    worker.args = worker.parser.parse_args()
    worker.config = {"model_dir": "models"}
    assert worker.find_model_directory() == Path("models")


@pytest.mark.parametrize(
    "model_path, exists, error",
    (
        [
            None,
            True,
            "No path to the model was provided. Please provide model_dir either through configuration or as CLI argument.",
        ],
        ["models", False, "The path models does not link to any directory"],
    ),
)
def test_find_model_directory_not_found(monkeypatch, model_path, exists, error):
    if model_path:
        monkeypatch.setattr(sys, "argv", ["worker", "--model-dir", model_path])
    else:
        monkeypatch.setattr(sys, "argv", ["worker"])

    monkeypatch.setattr("pathlib.Path.exists", lambda x: exists)

    worker = BaseWorker()
    worker.args = worker.parser.parse_args()
    worker.config = {"model_dir": model_path}

    with pytest.raises(ModelNotFoundError, match=error):
        worker.find_model_directory()
