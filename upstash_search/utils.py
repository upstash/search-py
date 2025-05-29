import typing as t

from upstash_search.errors import ClientError
from upstash_search.types import Document


def documents_to_payload(
    documents: t.Sequence[t.Union[t.Dict[t.Any, t.Any], t.Tuple[t.Any, ...], Document]],
) -> t.List[t.Dict[str, t.Any]]:
    payload = []
    for doc in documents:
        parsed_doc = _parse_document(doc)
        payload.append(
            {
                "id": parsed_doc.id,
                "content": parsed_doc.content,
                "metadata": parsed_doc.metadata,
            }
        )

    return payload


def _parse_document(
    document: t.Union[t.Dict[t.Any, t.Any], t.Tuple[t.Any, ...], Document],
) -> Document:
    if isinstance(document, Document):
        return document
    elif isinstance(document, tuple):
        return _parse_tuple(document)
    elif isinstance(document, dict):
        return _parse_dict(document)
    else:
        raise ClientError(f"Unsupported document type: {document}")


def _parse_tuple(document: t.Tuple[t.Any, ...]) -> Document:
    if len(document) < 2:
        raise ClientError(
            "The tuple must contain at least two elements; "
            "one for id, and other for content."
        )

    doc_id = document[0]
    content = document[1]

    if len(document) > 2:
        metadata = document[2]
    else:
        metadata = None

    return Document(
        id=doc_id,
        content=content,
        metadata=metadata,
    )


def _parse_dict(document: t.Dict[t.Any, t.Any]) -> Document:
    doc_id = document["id"]
    content = document["content"]
    metadata = document.get("metadata")

    return Document(
        id=doc_id,
        content=content,
        metadata=metadata,
    )
