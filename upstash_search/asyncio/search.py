import os
import typing as t

from upstash_search.asyncio.http import AsyncRequester
from upstash_search.asyncio.index import AsyncIndex
from upstash_search.paths import LIST_INDEXES_PATH, DELETE_INDEX_PATH, INFO_PATH
from upstash_search.types import Info, parse_info


class AsyncSearch:
    """
    Upstash Search client that uses the HTTP API to perform operations.

    ```python
    from upstash_search import AsyncSearch

    client = AsyncSearch(
        url="UPSTASH_SEARCH_REST_URL",
        token="UPSTASH_SEARCH_REST_TOKEN",
    )
    index = client.index("INDEX_NAME")
    ```
    """

    def __init__(
        self,
        url: str,
        token: str,
        *,
        retries: int = 3,
        retry_interval: float = 1.0,
        allow_telemetry: bool = True,
    ):
        self._url = url
        self._requester = AsyncRequester(
            url=url,
            token=token,
            retries=retries,
            retry_interval=retry_interval,
            allow_telemetry=allow_telemetry,
        )

    def index(self, name: str) -> AsyncIndex:
        """
        Returns an index for the given name.

        Each index is an isolated component of a database where
        documents can be added, retrieved, searched, and deleted.

        :param name: Name of the index.
        """

        return AsyncIndex(name, self._requester)

    async def list_indexes(self) -> t.List[str]:
        """
        Returns the names of the indexes of the database.
        """

        indexes = await self._requester.post(
            path=LIST_INDEXES_PATH,
        )
        return indexes  # type: ignore[no-any-return]

    async def delete_index(self, name: str) -> None:
        """
        Deletes the given index of the database.

        :param name: Name of the index to delete.
        """

        await self._requester.post(
            path=DELETE_INDEX_PATH,
            index=name,
        )

    async def info(self) -> Info:
        """
        Returns the database info.
        """

        result = await self._requester.post(
            path=INFO_PATH,
        )

        return parse_info(result)

    @classmethod
    def from_env(
        cls,
        *,
        retries: int = 3,
        retry_interval: float = 1.0,
        allow_telemetry: bool = True,
    ) -> "AsyncSearch":
        """
        Load the credentials from environment variables,
        and returns a client.
        """

        return cls(
            url=os.environ["UPSTASH_SEARCH_REST_URL"],
            token=os.environ["UPSTASH_SEARCH_REST_TOKEN"],
            retries=retries,
            retry_interval=retry_interval,
            allow_telemetry=allow_telemetry,
        )
