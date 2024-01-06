# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

from collections.abc import AsyncGenerator

import aiohttp
import pytest_asyncio


@pytest_asyncio.fixture(scope="session")
async def session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    timeout = aiohttp.ClientTimeout(total=30)
    test_session = aiohttp.ClientSession(timeout=timeout)
    yield test_session
    await test_session.close()
