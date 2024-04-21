# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

""" Asynchronous wrapper for Repology API """

from repology_client.client import (
    api,
    get_packages,
    get_projects,
    resolve_package,
)

__all__ = [
    "api",
    "get_packages",
    "get_projects",
    "resolve_package",
]
