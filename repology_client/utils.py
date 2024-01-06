# SPDX-License-Identifier: EUPL-1.2 AND CC-BY-SA-3.0
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>
# SPDX-FileCopyrightText: 2017 Mark Amery <markrobertamery@gmail.com>

""" Utility functions and classes. """

import asyncio
import time
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Any

import aiohttp

from repology_client.constants import USER_AGENT


class limit():
    """
    Based on `this StackOverflow answer
    <https://stackoverflow.com/questions/35196974/aiohttp-set-maximum-number-of-requests-per-second/62503115>`_.

    Set a limit on requests per second.
    """

    def __init__(self, calls: int, period: float):
        """
        :param calls: number of calls
        :param period: time period in seconds
        """
        self.calls: int = calls
        self.period: float = period
        self.clock: Callable[[], float] = time.monotonic
        self.last_reset: float = 0.0
        self.num_calls: int = 0

    def __call__(self, func: Callable) -> Callable:
        async def wrapper(*args: Any, **kwargs: Any) -> Callable:
            if self.num_calls >= self.calls:
                await asyncio.sleep(self.__period_remaining())

            period_remaining = self.__period_remaining()

            if period_remaining <= 0:
                self.num_calls = 0
                self.last_reset = self.clock()

            self.num_calls += 1

            return await func(*args, **kwargs)

        return wrapper

    def __period_remaining(self) -> float:
        elapsed = self.clock() - self.last_reset
        return self.period - elapsed


@asynccontextmanager
async def ensure_session(
    session: aiohttp.ClientSession | None = None
) -> AsyncGenerator[aiohttp.ClientSession, None]:
    """
    Create a new client session, if necessary, and close it on exit.

    :param session: :external+aiohttp:py:module:`aiohttp` client session
    """

    keep_session = True
    if session is None:
        timeout = aiohttp.ClientTimeout(total=30)
        headers = {"user-agent": USER_AGENT}
        session = aiohttp.ClientSession(headers=headers, timeout=timeout)
        keep_session = False

    yield session

    if not keep_session:
        await session.close()
