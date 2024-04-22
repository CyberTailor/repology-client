# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

""" Common code for Repology API clients. """

import aiohttp

from repology_client.exceptions import EmptyResponse
from repology_client.utils import ensure_session, limit


@limit(calls=1, period=1.0)
async def _call(location: str, params: dict | None = None, *,
                session: aiohttp.ClientSession | None = None) -> bytes:
    """
    Do a single rate-limited request.

    :param location: URL location
    :param params: URL query string parameters
    :param session: :external+aiohttp:py:module:`aiohttp` client session

    :raises repology.exceptions.EmptyResponse: on empty response
    :raises aiohttp.ClientResponseError: on HTTP errors

    :returns: raw response
    """

    async with ensure_session(session) as aiohttp_session:
        async with aiohttp_session.get(location, params=params or {},
                                       raise_for_status=True) as response:
            data = await response.read()
            if not data:
                raise EmptyResponse

    return data
