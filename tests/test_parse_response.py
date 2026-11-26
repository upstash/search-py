import httpx
import pytest

from upstash_search.errors import UpstashError
from upstash_search.http import parse_response


def test_result() -> None:
    assert parse_response(httpx.Response(200, json={"result": [1, 2]})) == [1, 2]
    assert parse_response(httpx.Response(200, json={"result": None})) is None


def test_error_from_the_server() -> None:
    with pytest.raises(UpstashError, match="Unauthorized: Invalid auth token"):
        parse_response(
            httpx.Response(401, json={"error": "Unauthorized: Invalid auth token"})
        )


def test_empty_body() -> None:
    with pytest.raises(UpstashError, match="status 308 and an empty body"):
        parse_response(httpx.Response(308))


def test_body_that_is_not_json() -> None:
    with pytest.raises(UpstashError, match="status 502: <html>Bad Gateway</html>"):
        parse_response(httpx.Response(502, text="<html>Bad Gateway</html>"))


def test_json_body_that_is_not_an_object() -> None:
    with pytest.raises(UpstashError, match="status 200"):
        parse_response(httpx.Response(200, json=["unexpected"]))
