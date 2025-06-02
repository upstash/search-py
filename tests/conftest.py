import pytest
import pytest_asyncio

from tests import INDEX_NAME, URL, TOKEN
from upstash_search import Search, AsyncIndex, Index, AsyncSearch


@pytest.fixture
def search() -> Search:
    client = Search(url=URL, token=TOKEN)
    index = client.index(INDEX_NAME)
    index.reset()
    return client


@pytest.fixture
def index() -> Index:
    client = Search(url=URL, token=TOKEN)
    index = client.index(INDEX_NAME)
    index.reset()
    return index


@pytest_asyncio.fixture
async def async_search() -> AsyncSearch:
    client = AsyncSearch(url=URL, token=TOKEN)
    index = client.index(INDEX_NAME)
    await index.reset()
    return client


@pytest_asyncio.fixture
async def async_index() -> AsyncIndex:
    client = AsyncSearch(url=URL, token=TOKEN)
    index = client.index(INDEX_NAME)
    await index.reset()
    return index
