import pytest

from tests import INDEX_NAME
from upstash_search import AsyncSearch


@pytest.mark.asyncio
async def test_list_indexes_async(async_search: AsyncSearch) -> None:
    async_index = async_search.index(INDEX_NAME)
    await async_index.upsert(
        documents=[
            ("id-0", {"data": 0}),
        ],
    )
    indexes = await async_search.list_indexes()

    assert len(indexes) >= 1


@pytest.mark.asyncio
async def test_delete_index_async(async_search: AsyncSearch) -> None:
    name = INDEX_NAME + "!"
    another_index = async_search.index(name)
    await another_index.upsert(
        documents=[
            ("id-0", {"data": 0}),
        ],
    )

    indexes = await async_search.list_indexes()
    assert name in indexes

    await async_search.delete_index(name)

    indexes = await async_search.list_indexes()
    assert name not in indexes


@pytest.mark.asyncio
async def test_info_async(async_search: AsyncSearch) -> None:
    index = async_search.index(INDEX_NAME)
    await index.upsert(
        documents=[
            ("id-0", {"data": 0}),
        ],
    )

    info = await async_search.info()
    assert info.document_count > 0
    assert INDEX_NAME in info.indexes

    index_info = info.indexes[INDEX_NAME]
    assert index_info.document_count > 0
