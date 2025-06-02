import dataclasses
import typing as t


@dataclasses.dataclass
class Document:
    id: str
    content: t.Dict[t.Any, t.Any]
    metadata: t.Optional[t.Dict[t.Any, t.Any]] = None


def parse_document(result: t.Dict[t.Any, t.Any]) -> Document:
    return Document(
        id=result["id"],
        content=result["content"],
        metadata=result.get("metadata"),
    )


UpsertDocumentT = t.Union[
    Document,
    t.Dict[str, t.Any],
    t.Tuple[t.Any, ...],
]


@dataclasses.dataclass
class DocumentScore:
    id: str
    score: float
    content: t.Dict[t.Any, t.Any]
    metadata: t.Optional[t.Dict[t.Any, t.Any]] = None


def parse_document_score(result: t.Dict[t.Any, t.Any]) -> DocumentScore:
    return DocumentScore(
        id=result["id"],
        score=result["score"],
        content=result["content"],
        metadata=result.get("metadata"),
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
class Info:
    document_count: int
    pending_document_count: int
    disk_size: int
    indexes: t.Dict[str, IndexInfo]


def parse_info(result: t.Dict[t.Any, t.Any]) -> Info:
    return Info(
        document_count=result["vectorCount"],
        pending_document_count=result["pendingVectorCount"],
        disk_size=result["indexSize"],
        indexes={
            index: parse_index_info(index_info)
            for index, index_info in result["namespaces"].items()
        },
    )


def parse_deleted(result: t.Dict[t.Any, t.Any]) -> int:
    return result["deleted"]  # type: ignore[no-any-return]
