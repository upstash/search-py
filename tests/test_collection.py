from tests import INDEX_NAME
from upstash_search import Search


def test_list_indexes(search: Search) -> None:
    index = search.index(INDEX_NAME)
    index.upsert(
        documents=[
            ("id-0", {"data": 0}),
        ],
    )
    indexes = search.list_indexes()

    assert len(indexes) >= 1


def test_delete_index(search: Search) -> None:
    name = INDEX_NAME + "!"
    another_index = search.index(name)
    another_index.upsert(
        documents=[
            ("id-0", {"data": 0}),
        ],
    )

    indexes = search.list_indexes()
    assert name in indexes

    search.delete_index(name)

    indexes = search.list_indexes()
    assert name not in indexes


def test_info(search: Search) -> None:
    index = search.index(INDEX_NAME)
    index.upsert(
        documents=[
            ("id-0", {"data": 0}),
        ],
    )

    info = search.info()
    assert info.document_count > 0
    assert INDEX_NAME in info.indexes

    index_info = info.indexes[INDEX_NAME]
    assert index_info.document_count > 0
