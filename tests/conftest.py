import pytest
import pytest_asyncio

from tests import INDEX_NAME, URL, TOKEN
from upstash_search import Collection, AsyncIndex, Index, AsyncCollection


@pytest.fixture
def collection() -> Collection:
    collection = Collection(url=URL, token=TOKEN)
    index = collection.index(INDEX_NAME)
    index.reset()
    return collection


@pytest.fixture
def index() -> Index:
    collection = Collection(url=URL, token=TOKEN)
    index = collection.index(INDEX_NAME)
    index.reset()
    return index


@pytest_asyncio.fixture
async def async_collection() -> AsyncCollection:
    collection = AsyncCollection(url=URL, token=TOKEN)
    index = collection.index(INDEX_NAME)
    await index.reset()
    return collection


@pytest_asyncio.fixture
async def async_index() -> AsyncIndex:
    collection = AsyncCollection(url=URL, token=TOKEN)
    index = collection.index(INDEX_NAME)
    await index.reset()
    return index
