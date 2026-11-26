import pytest

from upstash_search.errors import ClientError
from upstash_search.http import request_url

URL = "https://example.upstash.io"


def test_without_index() -> None:
    assert request_url(URL, "/info") == f"{URL}/info"
    assert request_url(URL, "/info", None) == f"{URL}/info"
    assert request_url(URL, "/reset", "") == f"{URL}/reset"


def test_plain_index_name() -> None:
    assert request_url(URL, "/search", "movies") == f"{URL}/search/movies"
    assert request_url(URL, "/search", "my-index_1.v2") == f"{URL}/search/my-index_1.v2"


@pytest.mark.parametrize(
    "name,encoded",
    [
        ("my index", "my%20index"),
        ("a?b", "a%3Fb"),
        ("a#b", "a%23b"),
        ("a&b=c", "a%26b%3Dc"),
        ("ürün", "%C3%BCr%C3%BCn"),
        ("...", "..."),
    ],
)
def test_special_characters_stay_in_the_name(name: str, encoded: str) -> None:
    assert request_url(URL, "/search", name) == f"{URL}/search/{encoded}"


@pytest.mark.parametrize(
    "name",
    [".", "..", "a/b", "a\\b", "a%2Fb", "a\nb", "a\tb", "a\x7fb"],
)
def test_names_that_cannot_be_used(name: str) -> None:
    with pytest.raises(ClientError):
        request_url(URL, "/search", name)


def test_non_string_name() -> None:
    with pytest.raises(ClientError):
        request_url(URL, "/search", 5)  # type: ignore[arg-type]
