import os
import platform as p
import time
import typing as t

import httpx

from upstash_search import __version__
from upstash_search.errors import UpstashError


def generate_headers(token: str, allow_telemetry: bool) -> t.Dict[str, str]:
    headers = {
        "Authorization": f"Bearer {token}",
    }

    if allow_telemetry:
        headers["Upstash-Telemetry-Sdk"] = f"upstash-search-py@v{__version__}"
        headers["Upstash-Telemetry-Runtime"] = f"python@v{p.python_version()}"

        if os.getenv("VERCEL"):
            platform = "vercel"
        elif os.getenv("AWS_REGION"):
            platform = "aws"
        else:
            platform = "unknown"

        headers["Upstash-Telemetry-Platform"] = platform

    return headers


class Requester:
    def __init__(
        self,
        url: str,
        token: str,
        retries: int,
        retry_interval: float,
        allow_telemetry: bool,
    ):
        self._client = httpx.Client(
            timeout=httpx.Timeout(
                timeout=600.0,
                connect=10.0,
            )
        )
        self._url = url
        self._headers = generate_headers(token, allow_telemetry)
        self._retries = retries
        self._retry_interval = retry_interval

    def post(
        self,
        path: str,
        payload: t.Optional[t.Any] = None,
        index: t.Optional[str] = None,
    ) -> t.Any:
        if index:
            url = f"{self._url}{path}/{index}"
        else:
            url = f"{self._url}{path}"

        response = None
        last_error = None

        for attempts_left in range(max(0, self._retries), -1, -1):
            try:
                response = self._client.post(
                    url=url,
                    headers=self._headers,
                    json=payload,
                )
                break

            except Exception as e:
                last_error = e
                if attempts_left > 0:
                    time.sleep(self._retry_interval)

        if response is None:
            assert last_error is not None
            raise last_error

        body = response.json()
        if "error" in body:
            raise UpstashError(body["error"])

        return body["result"]
