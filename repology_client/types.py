# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

""" Type definitions for Repology API, implemented as Pydantic models. """

from pydantic.dataclasses import dataclass


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
