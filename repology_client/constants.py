# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

"""
Hardcoded constants for rapidly-changing Repology API. What could possibly go
wrong?
"""

# Library package name.
PACKAGE = "repology-client"

# Library version.
VERSION = "0.0.1"

# Library homepage.
HOMEPAGE = "https://repology-client.sysrq.in"

# Library's User-agent header
USER_AGENT = f"Mozilla/5.0 (compatible; {PACKAGE}/{VERSION}; +{HOMEPAGE})"

# Base URL for all API requests.
API_URL = "https://repology.org/api/v1"

# Maximum number of projects API can return.
MAX_PROJECTS = 200

# Number of projects, starting from which you should use bulk export instead.
HARD_LIMIT = 5_000
