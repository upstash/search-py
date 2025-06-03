import pytest

from tests import assert_eventually
from upstash_search import Index
from upstash_search.types import Document


def test_upsert(index: Index) -> None:
    index.upsert(
        documents=[
            ("id-0", {"data": 0}),
            ("id-1", {"data": 1}, {"key": "value-1"}),
            {"id": "id-2", "content": {"data": 2}},
            {"id": "id-3", "content": {"data": 3}, "metadata": {"key": "value-3"}},
            Document(id="id-4", content={"data": 4}),
            Document(id="id-5", content={"data": 5}, metadata={"key": "value-5"}),
        ]
    )

    documents = index.fetch(
        ids=["id-0", "id-1", "id-2", "id-3", "id-4", "id-5"],
    )

    assert len(documents) == 6

    assert documents[0] is not None
    assert documents[0].id == "id-0"
    assert documents[0].content == {"data": 0}
    assert documents[0].metadata is None

    assert documents[1] is not None
    assert documents[1].id == "id-1"
    assert documents[1].content == {"data": 1}
    assert documents[1].metadata == {"key": "value-1"}

    assert documents[2] is not None
    assert documents[2].id == "id-2"
    assert documents[2].content == {"data": 2}
    assert documents[2].metadata is None

    assert documents[3] is not None
    assert documents[3].id == "id-3"
    assert documents[3].content == {"data": 3}
    assert documents[3].metadata == {"key": "value-3"}

    assert documents[4] is not None
    assert documents[4].id == "id-4"
    assert documents[4].content == {"data": 4}
    assert documents[4].metadata is None

    assert documents[5] is not None
    assert documents[5].id == "id-5"
    assert documents[5].content == {"data": 5}
    assert documents[5].metadata == {"key": "value-5"}


def test_upsert_single(index: Index) -> None:
    index.upsert(
        ("id-0", {"data": 0}),
    )

    index.upsert(
        {"id": "id-1", "content": {"data": 1}, "metadata": {"key": "value-1"}},
    )

    index.upsert(
        Document(id="id-2", content={"data": 2}),
    )

    documents = index.fetch(
        ids=["id-0", "id-1", "id-2"],
    )

    assert len(documents) == 3

    assert documents[0] is not None
    assert documents[0].id == "id-0"
    assert documents[0].content == {"data": 0}
    assert documents[0].metadata is None

    assert documents[1] is not None
    assert documents[1].id == "id-1"
    assert documents[1].content == {"data": 1}
    assert documents[1].metadata == {"key": "value-1"}

    assert documents[2] is not None
    assert documents[2].id == "id-2"
    assert documents[2].content == {"data": 2}
    assert documents[2].metadata is None


def test_upsert_invalid_tuple_or_dict(index: Index) -> None:
    with pytest.raises(Exception):
        index.upsert(documents=[("id",)])

    with pytest.raises(Exception):
        index.upsert(documents=[{"id": "id-0"}])

    with pytest.raises(Exception):
        index.upsert(documents=[{"content": {"data": 4}}])

    with pytest.raises(Exception):
        index.upsert(documents=["something else"])  # type: ignore[list-item]


def test_search(index: Index) -> None:
    index.upsert(
        documents=[
            ("id-0", {"data": 0}),
            ("id-1", {"data": 1}, {"key": 1}),
            ("i-d-2", {"data": 2}, {"key": 2}),
        ]
    )

    def assertion() -> None:
        scores = index.search(
            "data 1",
            limit=1,
        )
        assert len(scores) == 1

        assert scores[0].id == "id-1"
        assert scores[0].score > 0.0
        assert scores[0].content == {"data": 1}
        assert scores[0].metadata == {"key": 1}

    assert_eventually(assertion)


def test_search_filter(index: Index) -> None:
    index.upsert(
        documents=[
            ("id-0", {"data": 0}),
            ("id-1", {"data": 1}, {"key": 1}),
            ("id-2", {"data": 2}, {"key": 2}),
        ]
    )

    def assertion() -> None:
        scores = index.search(
            "data 1",
            limit=1,
            filter="data = 2",
        )
        assert len(scores) == 1

        assert scores[0].id == "id-2"
        assert scores[0].score > 0.0
        assert scores[0].content == {"data": 2}
        assert scores[0].metadata == {"key": 2}

    assert_eventually(assertion)


def test_fetch(index: Index) -> None:
    index.upsert(
        documents=[
            ("id-0", {"data": 0}),
            ("id-1", {"data": 1}, {"key": "value-1"}),
        ]
    )

    documents = index.fetch(
        ids=["id-0", "id-1", "id-2"],
    )

    assert len(documents) == 3

    assert documents[0] is not None
    assert documents[0].id == "id-0"
    assert documents[0].content == {"data": 0}
    assert documents[0].metadata is None

    assert documents[1] is not None
    assert documents[1].id == "id-1"
    assert documents[1].content == {"data": 1}
    assert documents[1].metadata == {"key": "value-1"}

    assert documents[2] is None


def test_fetch_with_prefix(index: Index) -> None:
    index.upsert(
        documents=[
            ("id-0", {"data": 0}),
            ("id-1", {"data": 1}, {"key": "value-1"}),
            ("i-d-2", {"data": 2}, {"key": "value-2"}),
        ]
    )

    documents = index.fetch(
        prefix="i-",
    )

    assert len(documents) == 1

    assert documents[0] is not None
    assert documents[0].id == "i-d-2"
    assert documents[0].content == {"data": 2}
    assert documents[0].metadata == {"key": "value-2"}


def test_delete(index: Index) -> None:
    index.upsert(
        documents=[
            ("id-0", {"data": 0}),
            ("id-1", {"data": 1}, {"key": "value-1"}),
        ]
    )

    deleted = index.delete(
        ids=["id-0", "id-1", "id-2"],
    )
    assert deleted == 2

    documents = index.fetch(
        ids=["id-0", "id-1", "id-2"],
    )

    assert len(documents) == 3
    assert documents[0] is None
    assert documents[1] is None
    assert documents[2] is None


def test_delete_prefix(index: Index) -> None:
    index.upsert(
        documents=[
            ("id-0", {"data": 0}),
            ("id-1", {"data": 1}, {"key": "value-1"}),
            ("i-d-2", {"data": 2}, {"key": "value-2"}),
        ]
    )

    deleted = index.delete(
        prefix="i-d",
    )
    assert deleted == 1

    documents = index.fetch(
        ids=["i-d-2"],
    )

    assert len(documents) == 1
    assert documents[0] is None


def test_delete_filter(index: Index) -> None:
    index.upsert(
        documents=[
            ("id-0", {"data": 0}, {"key": 0}),
            ("id-1", {"data": 1}, {"key": 1}),
            ("id-2", {"data": 2}, {"key": 2}),
        ]
    )

    deleted = index.delete(
        filter="data >= 1",
    )
    assert deleted == 2

    documents = index.fetch(
        ids=["id-0", "id-1", "id-2"],
    )

    assert len(documents) == 3
    assert documents[0] is not None
    assert documents[1] is None
    assert documents[2] is None


def test_range(index: Index) -> None:
    index.upsert(
        documents=[
            ("id-0", {"data": 0}, {"key": 0}),
            ("id-1", {"data": 1}, {"key": 1}),
            ("id-2", {"data": 2}, {"key": 2}),
        ]
    )

    range_documents = index.range(
        cursor="",
        limit=1,
    )

    assert range_documents.next_cursor != ""
    assert len(range_documents.documents) == 1

    assert range_documents.documents[0].id == "id-0"
    assert range_documents.documents[0].content == {"data": 0}
    assert range_documents.documents[0].metadata == {"key": 0}

    range_documents = index.range(
        cursor=range_documents.next_cursor,
        limit=5,
    )

    assert range_documents.next_cursor == ""
    assert len(range_documents.documents) == 2

    assert range_documents.documents[0].id == "id-1"
    assert range_documents.documents[0].content == {"data": 1}
    assert range_documents.documents[0].metadata == {"key": 1}

    assert range_documents.documents[1].id == "id-2"
    assert range_documents.documents[1].content == {"data": 2}
    assert range_documents.documents[1].metadata == {"key": 2}


def test_range_prefix(index: Index) -> None:
    index.upsert(
        documents=[
            ("id-0", {"data": 0}, {"key": 0}),
            ("id-1", {"data": 1}, {"key": 1}),
            ("i-d-2", {"data": 2}, {"key": 2}),
        ]
    )

    range_documents = index.range(
        cursor="",
        prefix="i-",
        limit=10,
    )

    assert range_documents.next_cursor == ""
    assert len(range_documents.documents) == 1

    assert range_documents.documents[0].id == "i-d-2"
    assert range_documents.documents[0].content == {"data": 2}
    assert range_documents.documents[0].metadata == {"key": 2}


def test_reset(index: Index) -> None:
    index.upsert(
        documents=[
            ("id-0", {"data": 0}),
            ("id-1", {"data": 1}, {"key": "value-1"}),
        ]
    )

    index.reset()

    documents = index.fetch(
        ids=["id-0", "id-1", "id-2"],
    )

    assert len(documents) == 3
    assert documents[0] is None
    assert documents[1] is None
    assert documents[2] is None
