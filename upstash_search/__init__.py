__version__ = "0.1.0"

from upstash_search.asyncio.collection import AsyncCollection
from upstash_search.asyncio.index import AsyncIndex
from upstash_search.collection import Collection
from upstash_search.index import Index

__all__ = ["Collection", "Index", "AsyncCollection", "AsyncIndex"]
