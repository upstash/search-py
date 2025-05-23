from tests import INDEX_NAME
from upstash_search import Collection


def test_list_indexes(collection: Collection) -> None:
    index = collection.index(INDEX_NAME)
    index.upsert(
        documents=[
            ("id-0", "data"),
        ],
    )
    indexes = collection.list_indexes()

    assert len(indexes) >= 1


def test_delete_index(collection: Collection) -> None:
    name = INDEX_NAME + "!"
    another_index = collection.index(name)
    another_index.upsert(
        documents=[
            ("id-0", "data"),
        ],
    )

    indexes = collection.list_indexes()
    assert name in indexes

    collection.delete_index(name)

    indexes = collection.list_indexes()
    assert name not in indexes


def test_info(collection: Collection) -> None:
    index = collection.index(INDEX_NAME)
    index.upsert(
        documents=[
            ("id-0", "data"),
        ],
    )

    info = collection.info()
    assert info.document_count > 0
    assert INDEX_NAME in info.indexes

    index_info = info.indexes[INDEX_NAME]
    assert index_info.document_count > 0
