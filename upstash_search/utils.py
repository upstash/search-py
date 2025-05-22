import typing as t

from upstash_search.errors import ClientError
from upstash_search.types import UpsertDocument


def documents_to_payload(
    documents: t.Sequence[
        t.Union[t.Dict[t.Any, t.Any], t.Tuple[t.Any, ...], UpsertDocument]
    ],
) -> t.List[t.Dict[str, t.Any]]:
    payload = []
    for doc in documents:
        parsed_doc = _parse_document(doc)
        payload.append(
            {
                "id": parsed_doc.id,
                "data": parsed_doc.data,
                "metadata": parsed_doc.fields,
            }
        )

    return payload


def _parse_document(
    document: t.Union[t.Dict[t.Any, t.Any], t.Tuple[t.Any, ...], UpsertDocument],
) -> UpsertDocument:
    if isinstance(document, UpsertDocument):
        return document
    elif isinstance(document, tuple):
        return _parse_tuple(document)
    elif isinstance(document, dict):
        return _parse_dict(document)
    else:
        raise ClientError(f"Unsupported document type: {document}")


def _parse_tuple(document: t.Tuple[t.Any, ...]) -> UpsertDocument:
    if len(document) < 2:
        raise ClientError(
            "The tuple must contain at least two elements; "
            "one for id, and other for data."
        )

    doc_id = document[0]
    data = document[1]

    if len(document) > 2:
        fields = document[2]
    else:
        fields = None

    return UpsertDocument(
        id=doc_id,
        data=data,
        fields=fields,
    )


def _parse_dict(document: t.Dict[t.Any, t.Any]) -> UpsertDocument:
    doc_id = document["id"]
    data = document["data"]
    fields = document.get("fields")

    return UpsertDocument(
        id=doc_id,
        data=data,
        fields=fields,
    )
