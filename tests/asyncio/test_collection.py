import pytest

from tests import INDEX_NAME
from upstash_search import AsyncCollection


@pytest.mark.asyncio
async def test_list_indexes_async(async_collection: AsyncCollection) -> None:
    indexes = await async_collection.list_indexes()

    assert len(indexes) >= 1


@pytest.mark.asyncio
async def test_delete_index_async(async_collection: AsyncCollection) -> None:
    name = INDEX_NAME + "!"
    another_index = async_collection.index(name)
    await another_index.upsert(
        documents=[
            ("id-0", "data"),
        ],
    )

    indexes = await async_collection.list_indexes()
    assert name in indexes

    await async_collection.delete_index(name)

    indexes = await async_collection.list_indexes()
    assert name not in indexes


@pytest.mark.asyncio
async def test_info_async(async_collection: AsyncCollection) -> None:
    index = async_collection.index(INDEX_NAME)
    await index.upsert(
        documents=[
            ("id-0", "data"),
        ],
    )

    info = await async_collection.info()
    assert info.document_count > 0
    assert INDEX_NAME in info.indexes

    index_info = info.indexes[INDEX_NAME]
    assert index_info.document_count > 0
