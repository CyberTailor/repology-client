# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

""" Type definitions for Repology API, implemented as Pydantic models. """

from enum import StrEnum

from pydantic.dataclasses import dataclass


_DistromapPackages = tuple[str, ...]
_DistromapGroups = tuple[_DistromapPackages, _DistromapPackages]
Distromap = tuple[_DistromapGroups, ...]


class ResolvePackageType(StrEnum):
    """
    Package type enum for the "Project by package name" tool.
    """

    SOURCE = "srcname"
    BINARY = "binname"


@dataclass
class _ResolvePkg:
    """
    Internal object used in the :py:func:`repology_client.resolve_package`
    function to pass data into exceptions.
    """

    repo: str
    name: str
    name_type: ResolvePackageType

    def __str__(self) -> str:
        message_tmpl = "*{}* package '{}' in repository '{}'"
        return message_tmpl.format(
            "binary" if self.name_type == ResolvePackageType.BINARY else "source",
            self.name, self.repo
        )


@dataclass
class ProjectsRange:
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

    start: str = ""
    end: str = ""

    def __bool__(self) -> bool:
        return bool(self.start or self.end)

    def __str__(self) -> str:
        if self.end:
            return f"{self.start}..{self.end}"
        if self.start:
            return self.start
        return ""


@dataclass(frozen=True)
class Package:
    """
    Package description type returned by ``/api/v1/projects/`` endpoint.
    """

    # Required fields
    repo: str
    visiblename: str
    version: str
    status: str

    # Optional fields
    subrepo: str | None = None
    srcname: str | None = None
    binname: str | None = None
    origversion: str | None = None
    summary: str | None = None
    categories: frozenset[str] | None = None
    licenses: frozenset[str] | None = None
    maintainers: frozenset[str] | None = None
