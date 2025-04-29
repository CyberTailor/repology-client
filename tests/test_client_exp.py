# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

import uuid

import aiohttp
import pytest

import repology_client
from repology_client.exceptions import (
    EmptyResponse,
    InvalidInput,
)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_raw_api(session: aiohttp.ClientSession):
    updates = await repology_client.exp.api("/updates", session=session)
    assert len(updates) != 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_distromap_invalid(session: aiohttp.ClientSession):
    with pytest.raises(InvalidInput):
        await repology_client.exp.distromap("foo", "", session=session)

    with pytest.raises(InvalidInput):
        await repology_client.exp.distromap("foo", "foo", session=session)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_distromap_empty(session: aiohttp.ClientSession):
    fromrepo = uuid.uuid5(uuid.NAMESPACE_DNS, "fromrepo.invalid.domain").hex
    torepo = uuid.uuid5(uuid.NAMESPACE_DNS, "torepo.invalid.domain").hex

    with pytest.raises(EmptyResponse):
        await repology_client.exp.distromap(fromrepo, torepo, session=session)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_distromap(session: aiohttp.ClientSession):
    data = await repology_client.exp.distromap("pypi", "freebsd", session=session)
    assert (('pydantic',), ('devel/py-pydantic',)) in data
