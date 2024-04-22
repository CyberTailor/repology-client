# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

""" Asynchronous wrapper for Repology API (experimental endpoints). """

import json
from typing import Any

import aiohttp
from pydantic import TypeAdapter

from repology_client._client import _call
from repology_client.constants import API_EXP_URL
from repology_client.exceptions import (
    EmptyResponse,
    InvalidInput,
)
from repology_client.types import Distromap
from repology_client.utils import ensure_session


async def api(endpoint: str, params: dict | None = None, *,
              session: aiohttp.ClientSession | None = None) -> Any:
    """
    Do a single Experimental API request.

    :param endpoint: API endpoint (example: ``/distromap``)
    :param params: URL query string parameters
    :param session: :external+aiohttp:py:module:`aiohttp` client session

    :raises repology.exceptions.EmptyResponse: on empty response
    :raises aiohttp.ClientResponseError: on HTTP errors
    :raises json.JSONDecodeError: on JSON decode failure

    :returns: decoded JSON response
    """

    raw_data = await _call(API_EXP_URL + endpoint, params, session=session)
    data = json.loads(raw_data)
    if not data:
        raise EmptyResponse

    return data


async def distromap(fromrepo: str, torepo: str, *,
                    session: aiohttp.ClientSession | None = None) -> Distromap:
    """
    Access the ``/api/experimental/distromap`` endpoint to create intermapping
    of packages between repositories.

    :param fromrepo: first repository
    :param torepo: second repository
    :param session: :external+aiohttp:py:module:`aiohttp` client session

    :raises repology.exceptions.EmptyResponse: on empty response
    :raises repology.exceptions.InvalidInput: if repositories are no different
    or one of them is an empty string
    :raises aiohttp.ClientResponseError: on HTTP errors

    :returns: decoded API response
    """

    if not all([fromrepo, torepo]):
        raise InvalidInput("Got empty string as repository name")

    if fromrepo == torepo:
        raise InvalidInput("Given repositories are no different")

    params = {
        "fromrepo": fromrepo,
        "torepo": torepo,
    }

    async with ensure_session(session) as aiohttp_session:
        data = await api("/distromap", params=params, session=aiohttp_session)

    DistromapAdapter = TypeAdapter(Distromap)
    return DistromapAdapter.validate_python(data)
