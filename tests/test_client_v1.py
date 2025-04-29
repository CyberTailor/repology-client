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

import tests.common


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_raw_api(session: aiohttp.ClientSession):
    problems = await repology_client.api("/repository/freebsd/problems",
                                         session=session)
    assert len(problems) != 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_get_packages_empty(session: aiohttp.ClientSession):
    with pytest.raises(InvalidInput):
        await repology_client.get_packages("", session=session)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_get_packages_notfound(session: aiohttp.ClientSession):
    with pytest.raises(EmptyResponse):
        project = uuid.uuid5(uuid.NAMESPACE_DNS, "repology.org").hex
        await repology_client.get_packages(project, session=session)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_get_packages(session: aiohttp.ClientSession):
    packages = await repology_client.get_packages("firefox", session=session)
    tests.common.check_firefox_project(packages)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_get_projects_simple(session: aiohttp.ClientSession):
    projects = await repology_client.get_projects(count=200, session=session)
    assert len(projects) == 200


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_get_400_projects(session: aiohttp.ClientSession):
    projects = await repology_client.get_projects(count=400, session=session)
    assert len(projects) > 200


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_get_projects_start_and_end(session: aiohttp.ClientSession):
    with pytest.warns(UserWarning):
        await repology_client.get_projects("a", "b", session=session)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_get_projects_search_failed(session: aiohttp.ClientSession):
    with pytest.raises(EmptyResponse):
        project = uuid.uuid5(uuid.NAMESPACE_DNS, "repology.org").hex
        await repology_client.get_projects(search=project, session=session)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_get_projects_search(session: aiohttp.ClientSession):
    projects = await repology_client.get_projects(search="firefox", session=session)
    assert "firefox" in projects
