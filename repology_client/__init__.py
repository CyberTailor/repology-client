# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

""" Asynchronous wrapper for Repology API """

from types import SimpleNamespace

from repology_client._client import (
    api,
    get_packages,
    get_projects,
    resolve_package,
)
from repology_client._client.experimental import (
    api as api_exp,
    distromap,
)

exp = SimpleNamespace()
exp.api = api_exp
exp.distromap = distromap

__all__ = [
    "api",
    "get_packages",
    "get_projects",
    "resolve_package",

    "exp",
]
