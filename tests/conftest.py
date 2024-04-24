# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

from collections.abc import AsyncGenerator

import aiohttp
import pytest
import pytest_asyncio


@pytest_asyncio.fixture(scope="session")
async def session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    timeout = aiohttp.ClientTimeout(total=30)
    test_session = aiohttp.ClientSession(timeout=timeout)
    try:
        yield test_session
    finally:
        await test_session.close()


@pytest.fixture(autouse=True)
def vcr_config():
    return {"allowed_hosts": [r"repology\.org"]}
