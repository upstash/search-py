import asyncio
import typing as t

import httpx

from upstash_search.errors import UpstashError
from upstash_search.http import generate_headers, request_url


class AsyncRequester:
    def __init__(
        self,
        url: str,
        token: str,
        retries: int,
        retry_interval: float,
        allow_telemetry: bool,
    ):
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                timeout=600.0,
                connect=10.0,
            )
        )
        self._url = url
        self._headers = generate_headers(token, allow_telemetry)
        self._retries = retries
        self._retry_interval = retry_interval

    async def post(
        self,
        path: str,
        payload: t.Optional[t.Any] = None,
        index: t.Optional[str] = None,
    ) -> t.Any:
        url = request_url(self._url, path, index)

        response = None
        last_error = None

        for attempts_left in range(max(0, self._retries), -1, -1):
            try:
                response = await self._client.post(
                    url=url,
                    headers=self._headers,
                    json=payload,
                )
                break

            except Exception as e:
                last_error = e
                if attempts_left > 0:
                    await asyncio.sleep(self._retry_interval)

        if response is None:
            assert last_error is not None
            raise last_error

        body = response.json()
        if "error" in body:
            raise UpstashError(body["error"])

        return body["result"]
