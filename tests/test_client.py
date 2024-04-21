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
from repology_client.exceptions.resolve import (
    MultipleProjectsFound,
    ProjectNotFound,
)
from repology_client.types import (
    Package,
    ResolvePackageType,
)


def check_firefox_project(packages: set[Package]):
    """
    Check data returned by the ``/api/v1/project/firefox`` endpoint.
    """

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
async def test_raw_api(session: aiohttp.ClientSession):
    problems = await repology_client.api("/repository/freebsd/problems",
                                         session=session)
    assert len(problems) != 0


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_packages_empty(session: aiohttp.ClientSession):
    with pytest.raises(InvalidInput):
        await repology_client.get_packages("", session=session)


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_packages_notfound(session: aiohttp.ClientSession):
    with pytest.raises(EmptyResponse):
        project = uuid.uuid5(uuid.NAMESPACE_DNS, "repology.org").hex
        await repology_client.get_packages(project, session=session)


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_packages(session: aiohttp.ClientSession):
    packages = await repology_client.get_packages("firefox", session=session)
    check_firefox_project(packages)


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_projects_simple(session: aiohttp.ClientSession):
    projects = await repology_client.get_projects(count=200, session=session)
    assert len(projects) == 200


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_400_projects(session: aiohttp.ClientSession):
    projects = await repology_client.get_projects(count=400, session=session)
    assert len(projects) > 200


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_projects_start_and_end(session: aiohttp.ClientSession):
    with pytest.warns(UserWarning):
        await repology_client.get_projects("a", "b", session=session)


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_projects_search_failed(session: aiohttp.ClientSession):
    with pytest.raises(EmptyResponse):
        project = uuid.uuid5(uuid.NAMESPACE_DNS, "repology.org").hex
        await repology_client.get_projects(search=project, session=session)


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_get_projects_search(session: aiohttp.ClientSession):
    projects = await repology_client.get_projects(search="firefox", session=session)
    assert "firefox" in projects


@pytest.mark.vcr
@pytest.mark.skip(reason="vcrpy doesn't record a cassette")
@pytest.mark.asyncio(scope="session")
async def test_resolve_package_notfound(session: aiohttp.ClientSession):
    with pytest.raises(ProjectNotFound):
        repo = uuid.uuid5(uuid.NAMESPACE_DNS, "invalid.domain").hex
        await repology_client.resolve_package(repo, "firefox")

    with pytest.raises(ProjectNotFound):
        project = uuid.uuid5(uuid.NAMESPACE_DNS, "repology.org").hex
        await repology_client.resolve_package("freebsd", project)


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_resolve_package_multiple(session: aiohttp.ClientSession):
    with pytest.raises(MultipleProjectsFound) as exc:
        # example from https://github.com/renovatebot/renovate/issues/11435
        await repology_client.resolve_package(
            "ubuntu_20_04", "gcc", ResolvePackageType.BINARY,
            autoresolve=False
        )
    assert sorted(exc.value.names) == ["gcc-defaults", "gcc-defaults-mipsen"]


@pytest.mark.vcr
@pytest.mark.asyncio(scope="session")
async def test_resolve_package(session: aiohttp.ClientSession):
    packages = await repology_client.resolve_package("freebsd", "www/firefox")
    check_firefox_project(packages)
