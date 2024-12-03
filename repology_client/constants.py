# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

"""
Hardcoded constants for rapidly-changing Repology API. What could possibly go
wrong?
"""

#: Library package name.
PACKAGE = "repology-client"

#: Library version.
VERSION = "0.3.0"

#: Library homepage.
HOMEPAGE = "https://repology-client.sysrq.in"

#: Library's User-agent header
USER_AGENT = f"Mozilla/5.0 (compatible; {PACKAGE}/{VERSION}; +{HOMEPAGE})"

#: Base URL for API v1 requests.
API_V1_URL = "https://repology.org/api/v1"

#: Base URL for Experimental API requests.
API_EXP_URL = "https://repology.org/api/experimental"

#: Base URL for the "Project by package name" tool.
TOOL_PROJECT_BY_URL = "https://repology.org/tools/project-by"

#: Maximum number of projects API can return.
MAX_PROJECTS = 200

#: Number of projects, starting from which you should use bulk export instead.
HARD_LIMIT = 5_000
