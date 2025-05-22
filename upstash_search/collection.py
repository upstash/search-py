import os
import typing as t

from upstash_search.http import Requester
from upstash_search.index import Index
from upstash_search.paths import LIST_INDEXES_PATH, DELETE_INDEX_PATH, INFO_PATH
from upstash_search.types import CollectionInfo, parse_collection_info


class Collection:
    """
    Upstash Search collection client that uses the HTTP API to perform operations.

    ```python
    from upstash_search import Collection

    collection = Collection(
        url="UPSTASH_SEARCH_REST_URL",
        token="UPSTASH_SEARCH_REST_TOKEN",
    )
    index = collection.index("INDEX_NAME")
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
        self._requester = Requester(
            url=url,
            token=token,
            retries=retries,
            retry_interval=retry_interval,
            allow_telemetry=allow_telemetry,
        )

    def index(self, name: str) -> Index:
        """
        Returns an index for the given name.

        Each index is an isolated component of a collection where
        documents can be added, retrieved, searched, and deleted.

        :param name: Name of the index.
        """

        return Index(name, self._requester)

    def list_indexes(self) -> t.List[str]:
        """
        Returns the names of the indexes of the collection.
        """

        indexes = self._requester.post(
            path=LIST_INDEXES_PATH,
        )
        return indexes  # type: ignore[no-any-return]

    def delete_index(self, name: str) -> None:
        """
        Deletes the given index of the collection.

        :param name: Name of the index to delete.
        """

        self._requester.post(
            path=DELETE_INDEX_PATH,
            index=name,
        )

    def info(self) -> CollectionInfo:
        """
        Returns the collection info.
        """

        result = self._requester.post(
            path=INFO_PATH,
        )

        return parse_collection_info(result)

    @classmethod
    def from_env(
        cls,
        *,
        retries: int = 3,
        retry_interval: float = 1.0,
        allow_telemetry: bool = True,
    ) -> "Collection":
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
