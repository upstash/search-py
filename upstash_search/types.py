import dataclasses
import typing as t


@dataclasses.dataclass
class Document:
    id: str
    data: str
    fields: t.Optional[t.Dict[t.Any, t.Any]] = None


def parse_document(result: t.Dict[t.Any, t.Any]) -> Document:
    return Document(
        id=result["id"],
        data=result["data"],
        fields=result.get("metadata"),
    )


@dataclasses.dataclass
class DocumentScore:
    id: str
    score: float
    data: t.Optional[str] = None
    fields: t.Optional[t.Dict[t.Any, t.Any]] = None


def parse_document_score(result: t.Dict[t.Any, t.Any]) -> DocumentScore:
    return DocumentScore(
        id=result["id"],
        score=result["score"],
        data=result.get("data"),
        fields=result.get("metadata"),
    )


@dataclasses.dataclass
class RangeDocuments:
    next_cursor: str
    documents: t.List[Document]


def parse_range_documents(result: t.Dict[t.Any, t.Any]) -> RangeDocuments:
    return RangeDocuments(
        next_cursor=result["nextCursor"],
        documents=[parse_document(doc) for doc in result["vectors"]],
    )


@dataclasses.dataclass
class IndexInfo:
    document_count: int
    pending_document_count: int


def parse_index_info(result: t.Dict[t.Any, t.Any]) -> IndexInfo:
    return IndexInfo(
        document_count=result["vectorCount"],
        pending_document_count=result["pendingVectorCount"],
    )


@dataclasses.dataclass
class CollectionInfo:
    document_count: int
    pending_document_count: int
    collection_size: int
    indexes: t.Dict[str, IndexInfo]


def parse_collection_info(result: t.Dict[t.Any, t.Any]) -> CollectionInfo:
    return CollectionInfo(
        document_count=result["vectorCount"],
        pending_document_count=result["pendingVectorCount"],
        collection_size=result["indexSize"],
        indexes={
            index: parse_index_info(index_info)
            for index, index_info in result["namespaces"].items()
        },
    )


def parse_deleted(result: t.Dict[t.Any, t.Any]) -> int:
    return result["deleted"]  # type: ignore[no-any-return]
