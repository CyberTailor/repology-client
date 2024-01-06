# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

import uuid

import aiohttp
import pytest

import repology_client
from repology_client.exceptions import EmptyResponse, InvalidInput
from repology_client.types import Package


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_packages_empty(session: aiohttp.ClientSession) -> None:
    with pytest.raises(InvalidInput):
        await repology_client.get_packages("", session=session)


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_packages_notfound(session: aiohttp.ClientSession) -> None:
    with pytest.raises(EmptyResponse):
        project = uuid.uuid5(uuid.NAMESPACE_DNS, "repology.org").hex
        await repology_client.get_packages(project, session=session)


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_packages(session: aiohttp.ClientSession) -> None:
    packages = await repology_client.get_packages("firefox", session=session)

    firefox_pkg: Package | None = None
    for pkg in packages:
        if pkg.repo == "gentoo" and pkg.visiblename == "www-client/firefox":
            firefox_pkg = pkg
            break

    assert firefox_pkg is not None
    assert firefox_pkg.srcname == "www-client/firefox"
    assert firefox_pkg.summary == "Firefox Web Browser"

    assert firefox_pkg.maintainers is not None
    assert "mozilla@gentoo.org" in firefox_pkg.maintainers

    assert firefox_pkg.licenses is not None
    assert "MPL-2.0" in firefox_pkg.licenses


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_projects_simple(session: aiohttp.ClientSession) -> None:
    projects = await repology_client.get_projects(count=200, session=session)
    assert len(projects) == 200


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_projects_start_and_end(session: aiohttp.ClientSession) -> None:
    with pytest.warns(UserWarning):
        await repology_client.get_projects("a", "b", session=session)


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_projects_search_failed(session: aiohttp.ClientSession) -> None:
    with pytest.raises(EmptyResponse):
        project = uuid.uuid5(uuid.NAMESPACE_DNS, "repology.org").hex
        await repology_client.get_projects(search=project, session=session)


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_projects_search(session: aiohttp.ClientSession) -> None:
    projects = await repology_client.get_projects(search="firefox", session=session)
    assert "firefox" in projects
