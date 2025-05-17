# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024-2025 Anna <cyber@sysrq.in>

""" Type definitions for Repology API, implemented as Pydantic models. """

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


_DistromapPackages = tuple[str, ...]
_DistromapGroups = tuple[_DistromapPackages, _DistromapPackages]

#: Intermapping of packages between two repositories.
Distromap = tuple[_DistromapGroups, ...]


class ResolvePackageType(StrEnum):
    """
    Package type enum for the "Project by package name" tool.
    """

    SOURCE = "srcname"
    BINARY = "binname"


class _ResolvePkg(BaseModel):
    """
    Internal object used in the :py:func:`repology_client.resolve_package`
    function to pass data into exceptions.
    """
    model_config = ConfigDict(defer_build=True, frozen=True)

    #: Repository name.
    repo: str

    #: Package name.
    name: str

    #: Package type (source or binary).
    name_type: ResolvePackageType

    def __str__(self) -> str:
        message_tmpl = "*{}* package '{}' in repository '{}'"
        return message_tmpl.format(
            "binary" if self.name_type == ResolvePackageType.BINARY else "source",
            self.name, self.repo
        )


class ProjectsRange(BaseModel):
    """
    Object for constructing a string representation of range.

    >>> str(ProjectsRange())
    ''
    >>> str(ProjectsRange(start="firefox"))
    'firefox'
    >>> str(ProjectsRange(end="firefox"))
    '..firefox'
    >>> str(ProjectsRange(start="firefox", end="firefoxpwa"))
    'firefox..firefoxpwa'
    """
    model_config = ConfigDict(defer_build=True, extra="forbid",
                              validate_assignment=True)

    #: First project to be included in range.
    start: str = ""

    #: Last project to be included in range.
    end: str = ""

    def __bool__(self) -> bool:
        return bool(self.start or self.end)

    def __str__(self) -> str:
        if self.end:
            return f"{self.start}..{self.end}"
        if self.start:
            return self.start
        return ""


class Package(BaseModel):
    """
    Package description type returned by ``/api/v1/projects/`` endpoint.
    """
    model_config = ConfigDict(defer_build=True, frozen=True)

    # Required fields

    #: Name of repository for this package.
    repo: str
    #: Package name as shown to the user by Repology.
    visiblename: str
    #: Package version (sanitized, as shown by Repology).
    version: str
    #: Package status ('newest', 'unique', 'outdated', etc).
    status: str

    # Optional fields

    #: Name of subrepository (if applicable).
    subrepo: str | None = None
    #: Package name as used in repository - source package name.
    srcname: str | None = None
    #: Package name as used in repository - binary package name.
    binname: str | None = None
    #: Package version as in repository.
    origversion: str | None = None
    #: One-line description of the package.
    summary: str | None = None
    #: List of package categories.
    categories: frozenset[str] | None = None
    #: List of package licenses.
    licenses: frozenset[str] | None = None
    #: List of package maintainers.
    maintainers: frozenset[str] | None = None


class Problem(BaseModel):
    """
    Type for problem entries returned by ``/api/v1/repository/<repo>/problems``
    and ``/api/v1/maintainer/<maint>/problems-for-repo/<repo>`` endpoints.
    """
    model_config = ConfigDict(defer_build=True, frozen=True)

    # Required fields

    #: Problem type.
    type: str
    #: Additional details on the problem.
    data: dict
    #: Repology project name.
    project_name: str
    #: Normalized version as used by Repology.
    version: str
    #: Repository package version.
    rawversion: str

    # Optional fields

    #: Repository (source) package name.
    srcname: str | None = None
    #: Repository (binary) package name.
    binname: str | None = None
