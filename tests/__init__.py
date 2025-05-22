import asyncio
import os
import time
import typing as t

import dotenv

dotenv.load_dotenv()

URL = os.environ["UPSTASH_SEARCH_REST_URL"]
TOKEN = os.environ["UPSTASH_SEARCH_REST_TOKEN"]
INDEX_NAME = "index"


def assert_eventually(
    assertion: t.Callable[[], None],
    retry_delay: float = 0.5,
    timeout: float = 5.0,
) -> None:
    deadline = time.time() + timeout
    last_err = None

    while time.time() < deadline:
        try:
            assertion()
            return
        except AssertionError as e:
            last_err = e
            time.sleep(retry_delay)

    if last_err is None:
        raise AssertionError("Couldn't run the assertion")

    raise last_err


async def assert_eventually_async(
    assertion: t.Callable[[], t.Awaitable[None]],
    retry_delay: float = 0.5,
    timeout: float = 5.0,
) -> None:
    deadline = time.time() + timeout
    last_err = None

    while time.time() < deadline:
        try:
            await assertion()
            return
        except AssertionError as e:
            last_err = e
            await asyncio.sleep(retry_delay)

    if last_err is None:
        raise AssertionError("Couldn't run the assertion")

    raise last_err
