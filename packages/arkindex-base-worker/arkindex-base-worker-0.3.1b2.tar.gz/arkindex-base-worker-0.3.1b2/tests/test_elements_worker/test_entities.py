# -*- coding: utf-8 -*-
import json
from uuid import UUID

import pytest
from apistar.exceptions import ErrorResponse

from arkindex_worker.cache import (
    CachedElement,
    CachedEntity,
    CachedTranscription,
    CachedTranscriptionEntity,
)
from arkindex_worker.models import Element, Transcription
from arkindex_worker.worker import EntityType
from arkindex_worker.worker.transcription import TextOrientation

from . import BASE_API_CALLS


def test_create_entity_wrong_element(mock_elements_worker):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=None,
            name="Bob Bob",
            type=EntityType.Person,
        )
    assert (
        str(e.value)
        == "element shouldn't be null and should be an Element or CachedElement"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element="not element type",
            name="Bob Bob",
            type=EntityType.Person,
        )
    assert (
        str(e.value)
        == "element shouldn't be null and should be an Element or CachedElement"
    )


def test_create_entity_wrong_name(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name=None,
            type=EntityType.Person,
        )
    assert str(e.value) == "name shouldn't be null and should be of type str"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name=1234,
            type=EntityType.Person,
        )
    assert str(e.value) == "name shouldn't be null and should be of type str"


def test_create_entity_wrong_type(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=None,
        )
    assert str(e.value) == "type shouldn't be null and should be of type EntityType"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=1234,
        )
    assert str(e.value) == "type shouldn't be null and should be of type EntityType"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type="not_an_entity_type",
        )
    assert str(e.value) == "type shouldn't be null and should be of type EntityType"


def test_create_entity_wrong_corpus(monkeypatch, mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    # Triggering an error on metas param, not giving corpus should work since
    # ARKINDEX_CORPUS_ID environment variable is set on mock_elements_worker
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=EntityType.Person,
            metas="wrong metas",
        )
    assert str(e.value) == "metas should be of type dict"


def test_create_entity_wrong_metas(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=EntityType.Person,
            metas="wrong metas",
        )
    assert str(e.value) == "metas should be of type dict"


def test_create_entity_wrong_validated(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=EntityType.Person,
            validated="wrong validated",
        )
    assert str(e.value) == "validated should be of type bool"


def test_create_entity_api_error(responses, mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})
    responses.add(
        responses.POST,
        "http://testserver/api/v1/entity/",
        status=500,
    )

    with pytest.raises(ErrorResponse):
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=EntityType.Person,
        )

    assert len(responses.calls) == len(BASE_API_CALLS) + 5
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        # We retry 5 times the API call
        ("POST", "http://testserver/api/v1/entity/"),
        ("POST", "http://testserver/api/v1/entity/"),
        ("POST", "http://testserver/api/v1/entity/"),
        ("POST", "http://testserver/api/v1/entity/"),
        ("POST", "http://testserver/api/v1/entity/"),
    ]


def test_create_entity(responses, mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})
    responses.add(
        responses.POST,
        "http://testserver/api/v1/entity/",
        status=200,
        json={"id": "12345678-1234-1234-1234-123456789123"},
    )

    entity_id = mock_elements_worker.create_entity(
        element=elt,
        name="Bob Bob",
        type=EntityType.Person,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        ("POST", "http://testserver/api/v1/entity/"),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "name": "Bob Bob",
        "type": "person",
        "metas": {},
        "validated": None,
        "corpus": "11111111-1111-1111-1111-111111111111",
        "worker_version": "12341234-1234-1234-1234-123412341234",
    }
    assert entity_id == "12345678-1234-1234-1234-123456789123"


def test_create_entity_with_cache(responses, mock_elements_worker_with_cache):
    elt = CachedElement.create(id="12341234-1234-1234-1234-123412341234", type="thing")
    responses.add(
        responses.POST,
        "http://testserver/api/v1/entity/",
        status=200,
        json={"id": "12345678-1234-1234-1234-123456789123"},
    )

    entity_id = mock_elements_worker_with_cache.create_entity(
        element=elt,
        name="Bob Bob",
        type=EntityType.Person,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        ("POST", "http://testserver/api/v1/entity/"),
    ]

    assert json.loads(responses.calls[-1].request.body) == {
        "name": "Bob Bob",
        "type": "person",
        "metas": {},
        "validated": None,
        "corpus": "11111111-1111-1111-1111-111111111111",
        "worker_version": "12341234-1234-1234-1234-123412341234",
    }
    assert entity_id == "12345678-1234-1234-1234-123456789123"

    # Check that created entity was properly stored in SQLite cache
    assert list(CachedEntity.select()) == [
        CachedEntity(
            id=UUID("12345678-1234-1234-1234-123456789123"),
            type="person",
            name="Bob Bob",
            validated=False,
            metas={},
            worker_version_id=UUID("12341234-1234-1234-1234-123412341234"),
        )
    ]


def test_create_transcription_entity_wrong_transcription(mock_elements_worker):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription_entity(
            transcription=None,
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length=10,
        )
    assert str(e.value) == "transcription shouldn't be null and should be of type str"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription_entity(
            transcription=1234,
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length=10,
        )
    assert str(e.value) == "transcription shouldn't be null and should be of type str"


def test_create_transcription_entity_wrong_entity(mock_elements_worker):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription_entity(
            transcription="11111111-1111-1111-1111-111111111111",
            entity=None,
            offset=5,
            length=10,
        )
    assert str(e.value) == "entity shouldn't be null and should be of type str"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription_entity(
            transcription="11111111-1111-1111-1111-111111111111",
            entity=1234,
            offset=5,
            length=10,
        )
    assert str(e.value) == "entity shouldn't be null and should be of type str"


def test_create_transcription_entity_wrong_offset(mock_elements_worker):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription_entity(
            transcription="11111111-1111-1111-1111-111111111111",
            entity="11111111-1111-1111-1111-111111111111",
            offset=None,
            length=10,
        )
    assert str(e.value) == "offset shouldn't be null and should be a positive integer"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription_entity(
            transcription="11111111-1111-1111-1111-111111111111",
            entity="11111111-1111-1111-1111-111111111111",
            offset="not an int",
            length=10,
        )
    assert str(e.value) == "offset shouldn't be null and should be a positive integer"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription_entity(
            transcription="11111111-1111-1111-1111-111111111111",
            entity="11111111-1111-1111-1111-111111111111",
            offset=-1,
            length=10,
        )
    assert str(e.value) == "offset shouldn't be null and should be a positive integer"


def test_create_transcription_entity_wrong_length(mock_elements_worker):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription_entity(
            transcription="11111111-1111-1111-1111-111111111111",
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length=None,
        )
    assert (
        str(e.value)
        == "length shouldn't be null and should be a strictly positive integer"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription_entity(
            transcription="11111111-1111-1111-1111-111111111111",
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length="not an int",
        )
    assert (
        str(e.value)
        == "length shouldn't be null and should be a strictly positive integer"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription_entity(
            transcription="11111111-1111-1111-1111-111111111111",
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length=0,
        )
    assert (
        str(e.value)
        == "length shouldn't be null and should be a strictly positive integer"
    )


def test_create_transcription_entity_api_error(responses, mock_elements_worker):
    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=500,
    )

    with pytest.raises(ErrorResponse):
        mock_elements_worker.create_transcription_entity(
            transcription="11111111-1111-1111-1111-111111111111",
            entity="11111111-1111-1111-1111-111111111111",
            offset=5,
            length=10,
        )

    assert len(responses.calls) == len(BASE_API_CALLS) + 5
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        # We retry 5 times the API call
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
    ]


def test_create_transcription_entity_no_confidence(responses, mock_elements_worker):
    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=200,
        json={
            "entity": "11111111-1111-1111-1111-111111111111",
            "offset": 5,
            "length": 10,
        },
    )

    mock_elements_worker.create_transcription_entity(
        transcription="11111111-1111-1111-1111-111111111111",
        entity="11111111-1111-1111-1111-111111111111",
        offset=5,
        length=10,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "entity": "11111111-1111-1111-1111-111111111111",
        "offset": 5,
        "length": 10,
        "worker_version_id": "12341234-1234-1234-1234-123412341234",
    }


def test_create_transcription_entity_with_confidence(responses, mock_elements_worker):
    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=200,
        json={
            "entity": "11111111-1111-1111-1111-111111111111",
            "offset": 5,
            "length": 10,
            "confidence": 0.33,
        },
    )

    mock_elements_worker.create_transcription_entity(
        transcription="11111111-1111-1111-1111-111111111111",
        entity="11111111-1111-1111-1111-111111111111",
        offset=5,
        length=10,
        confidence=0.33,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "entity": "11111111-1111-1111-1111-111111111111",
        "offset": 5,
        "length": 10,
        "worker_version_id": "12341234-1234-1234-1234-123412341234",
        "confidence": 0.33,
    }


def test_create_transcription_entity_confidence_none(responses, mock_elements_worker):
    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=200,
        json={
            "entity": "11111111-1111-1111-1111-111111111111",
            "offset": 5,
            "length": 10,
            "confidence": None,
        },
    )

    mock_elements_worker.create_transcription_entity(
        transcription="11111111-1111-1111-1111-111111111111",
        entity="11111111-1111-1111-1111-111111111111",
        offset=5,
        length=10,
        confidence=None,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "entity": "11111111-1111-1111-1111-111111111111",
        "offset": 5,
        "length": 10,
        "worker_version_id": "12341234-1234-1234-1234-123412341234",
    }


def test_create_transcription_entity_with_cache(
    responses, mock_elements_worker_with_cache
):
    CachedElement.create(
        id=UUID("12341234-1234-1234-1234-123412341234"),
        type="page",
    )
    CachedTranscription.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        element=UUID("12341234-1234-1234-1234-123412341234"),
        text="Hello, it's me.",
        confidence=0.42,
        orientation=TextOrientation.HorizontalLeftToRight,
        worker_version_id=UUID("12341234-1234-1234-1234-123412341234"),
    )
    CachedEntity.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        type="person",
        name="Bob Bob",
        worker_version_id=UUID("12341234-1234-1234-1234-123412341234"),
    )

    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=200,
        json={
            "entity": "11111111-1111-1111-1111-111111111111",
            "offset": 5,
            "length": 10,
        },
    )

    mock_elements_worker_with_cache.create_transcription_entity(
        transcription="11111111-1111-1111-1111-111111111111",
        entity="11111111-1111-1111-1111-111111111111",
        offset=5,
        length=10,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "entity": "11111111-1111-1111-1111-111111111111",
        "offset": 5,
        "length": 10,
        "worker_version_id": "12341234-1234-1234-1234-123412341234",
    }

    # Check that created transcription entity was properly stored in SQLite cache
    assert list(CachedTranscriptionEntity.select()) == [
        CachedTranscriptionEntity(
            transcription=UUID("11111111-1111-1111-1111-111111111111"),
            entity=UUID("11111111-1111-1111-1111-111111111111"),
            offset=5,
            length=10,
            worker_version_id=UUID("12341234-1234-1234-1234-123412341234"),
        )
    ]


def test_create_transcription_entity_with_confidence_with_cache(
    responses, mock_elements_worker_with_cache
):
    CachedElement.create(
        id=UUID("12341234-1234-1234-1234-123412341234"),
        type="page",
    )
    CachedTranscription.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        element=UUID("12341234-1234-1234-1234-123412341234"),
        text="Hello, it's me.",
        confidence=0.42,
        orientation=TextOrientation.HorizontalLeftToRight,
        worker_version_id=UUID("12341234-1234-1234-1234-123412341234"),
    )
    CachedEntity.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        type="person",
        name="Bob Bob",
        worker_version_id=UUID("12341234-1234-1234-1234-123412341234"),
    )

    responses.add(
        responses.POST,
        "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        status=200,
        json={
            "entity": "11111111-1111-1111-1111-111111111111",
            "offset": 5,
            "length": 10,
            "confidence": 0.77,
        },
    )

    mock_elements_worker_with_cache.create_transcription_entity(
        transcription="11111111-1111-1111-1111-111111111111",
        entity="11111111-1111-1111-1111-111111111111",
        offset=5,
        length=10,
        confidence=0.77,
    )

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "POST",
            "http://testserver/api/v1/transcription/11111111-1111-1111-1111-111111111111/entity/",
        ),
    ]
    assert json.loads(responses.calls[-1].request.body) == {
        "entity": "11111111-1111-1111-1111-111111111111",
        "offset": 5,
        "length": 10,
        "worker_version_id": "12341234-1234-1234-1234-123412341234",
        "confidence": 0.77,
    }

    # Check that created transcription entity was properly stored in SQLite cache
    assert list(CachedTranscriptionEntity.select()) == [
        CachedTranscriptionEntity(
            transcription=UUID("11111111-1111-1111-1111-111111111111"),
            entity=UUID("11111111-1111-1111-1111-111111111111"),
            offset=5,
            length=10,
            worker_version_id=UUID("12341234-1234-1234-1234-123412341234"),
            confidence=0.77,
        )
    ]


def test_list_transcription_entities(fake_dummy_worker):
    transcription = Transcription({"id": "fake_transcription_id"})
    worker_version = "worker_version_id"
    fake_dummy_worker.api_client.add_response(
        "ListTranscriptionEntities",
        id=transcription.id,
        worker_version=worker_version,
        response={"id": "entity_id"},
    )
    assert fake_dummy_worker.list_transcription_entities(
        transcription, worker_version
    ) == {"id": "entity_id"}

    assert len(fake_dummy_worker.api_client.history) == 1
    assert len(fake_dummy_worker.api_client.responses) == 0


def test_list_corpus_entities(responses, mock_elements_worker):
    corpus_id = "11111111-1111-1111-1111-111111111111"
    responses.add(
        responses.GET,
        f"http://testserver/api/v1/corpus/{corpus_id}/entities/",
        json={
            "count": 1,
            "next": None,
            "results": [
                {
                    "id": "fake_entity_id",
                }
            ],
        },
    )

    # list is required to actually do the request
    assert list(mock_elements_worker.list_corpus_entities()) == [
        {
            "id": "fake_entity_id",
        }
    ]

    assert len(responses.calls) == len(BASE_API_CALLS) + 1
    assert [
        (call.request.method, call.request.url) for call in responses.calls
    ] == BASE_API_CALLS + [
        (
            "GET",
            f"http://testserver/api/v1/corpus/{corpus_id}/entities/",
        ),
    ]


@pytest.mark.parametrize(
    "wrong_name",
    [
        1234,
        12.5,
    ],
)
def test_list_corpus_entities_wrong_name(mock_elements_worker, wrong_name):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.list_corpus_entities(name=wrong_name)
    assert str(e.value) == "name should be of type str"


@pytest.mark.parametrize(
    "wrong_parent",
    [{"id": "element_id"}, 12.5, "blabla"],
)
def test_list_corpus_entities_wrong_parent(mock_elements_worker, wrong_parent):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.list_corpus_entities(parent=wrong_parent)
    assert str(e.value) == "parent should be of type Element"
