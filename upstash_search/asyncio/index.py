import typing as t

from upstash_search.asyncio.http import AsyncRequester
from upstash_search.paths import (
    UPSERT_PATH,
    SEARCH_PATH,
    FETCH_PATH,
    DELETE_PATH,
    RANGE_PATH,
    RESET_PATH,
)
from upstash_search.types import (
    DocumentScore,
    Document,
    RangeDocuments,
    parse_document_score,
    parse_document,
    parse_deleted,
    parse_range_documents,
    UpsertDocumentT,
)
from upstash_search.utils import documents_to_payload


class AsyncIndex:
    """
    Represents an index of a database.

    Each index is an isolated component of a database where
    documents can be added, retrieved, searched, and deleted.
    """

    def __init__(
        self,
        name: str,
        requester: AsyncRequester,
    ):
        self._name = name
        self._requester = requester

    async def upsert(
        self,
        documents: t.Union[UpsertDocumentT, t.List[UpsertDocumentT]],
    ) -> None:
        """
        Upserts(updates or inserts) documents.

        Documents are identified by their unique ids.
        If a document with the same id already exists, it
        will be updated. Otherwise, a new document will be
        inserted.

        :param documents: Documents to upsert.
        """
        if not isinstance(documents, list):
            documents = [documents]

        payload = documents_to_payload(documents)

        await self._requester.post(
            path=UPSERT_PATH,
            payload=payload,
            index=self._name,
        )

    async def search(
        self,
        query: str,
        *,
        limit: int = 10,
        filter: str = "",
        reranking: bool = False,
    ) -> t.List[DocumentScore]:
        """
        Searches for documents matching the given query text.

        :param query: Query text to search for.
        :param limit: Number of documents to return.
        :param filter: Content filter to narrow down results.
        :param reranking: Whether to perform reranking on the results or not.
        """

        payload = {
            "query": query,
            "topK": limit,
            "filter": filter,
            "reranking": reranking,
            "includeData": True,
            "includeMetadata": True,
        }

        result = await self._requester.post(
            path=SEARCH_PATH,
            payload=payload,
            index=self._name,
        )

        document_scores = [
            parse_document_score(document_score) for document_score in result
        ]
        return document_scores

    async def fetch(
        self,
        *,
        ids: t.Optional[t.Sequence[str]] = None,
        prefix: t.Optional[str] = None,
    ) -> t.List[t.Optional[Document]]:
        """
        Fetches documents for the given ids or id prefix.

        :param ids: List of document ids to fetch.
        :param prefix: Prefix of the document ids to fetch.
        """

        payload: t.Dict[str, t.Any] = {
            "includeData": True,
            "includeMetadata": True,
        }

        if ids is not None:
            payload["ids"] = ids

        if prefix is not None:
            payload["prefix"] = prefix

        result = await self._requester.post(
            path=FETCH_PATH,
            payload=payload,
            index=self._name,
        )

        documents = [parse_document(doc) if doc is not None else None for doc in result]
        return documents

    async def delete(
        self,
        *,
        ids: t.Optional[t.Sequence[str]] = None,
        prefix: t.Optional[str] = None,
        filter: t.Optional[str] = None,
    ) -> int:
        """
        Deletes the documents having the given ids,
        id prefix, or content matching with filter.

        Returns how many documents are deleted.

        :param ids: List of document ids to delete.
        :param prefix: Prefix of the document ids to delete.
        :param filter: Filter to delete documents with matching content.
        """

        payload: t.Dict[str, t.Any] = {}
        if ids is not None:
            payload["ids"] = ids

        if prefix is not None:
            payload["prefix"] = prefix

        if filter is not None:
            payload["filter"] = filter

        result = await self._requester.post(
            path=DELETE_PATH,
            payload=payload,
            index=self._name,
        )

        deleted = parse_deleted(result)
        return deleted

    async def range(
        self,
        *,
        cursor: str = "",
        limit: int = 1,
        prefix: t.Optional[str] = None,
    ) -> RangeDocuments:
        """
        Ranges over the documents, starting from the cursor,
        and returning at most limit many documents.

        It can be used for paginating the documents, using
        the next cursor to use from the return value.

        :param cursor: Cursor to start range from.
        :param limit: At most how many documents to return.
        :param prefix: Optional document id prefix to range over.
        """

        payload = {
            "cursor": cursor,
            "limit": limit,
            "includeData": True,
            "includeMetadata": True,
        }

        if prefix is not None:
            payload["prefix"] = prefix

        result = await self._requester.post(
            path=RANGE_PATH,
            payload=payload,
            index=self._name,
        )

        range_documents = parse_range_documents(result)
        return range_documents

    async def reset(self) -> None:
        """
        Deletes all documents from the index
        and resets it to its initial state.
        """

        await self._requester.post(
            path=RESET_PATH,
            payload=None,
            index=self._name,
        )
