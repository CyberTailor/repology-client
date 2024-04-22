# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

""" Common code for Repology API clients. """

from pathlib import PurePosixPath
from typing import Any
from urllib.parse import urlparse, urlunparse

import aiohttp
from pydantic_core import from_json

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

    :raises repology_client.exceptions.EmptyResponse: on empty response
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


async def _json_api(base_url: str, endpoint: str | None = None,
                    params: dict | None = None, *,
                    session: aiohttp.ClientSession | None = None) -> Any:
    """
    Do a single API request.

    :param base: base API URL
    :param endpoint: API endpoint
    :param params: URL query string parameters
    :param session: :external+aiohttp:py:module:`aiohttp` client session

    :raises repology_client.exceptions.EmptyResponse: on empty response
    :raises aiohttp.ClientResponseError: on HTTP errors
    :raises ValueError: on JSON decode failure

    :returns: decoded JSON response
    """

    url = urlparse(base_url)

    url_path = url.path
    if endpoint is not None:
        endpoint_path = PurePosixPath(endpoint).relative_to("/")
        url_path = str(PurePosixPath(url.path) / endpoint_path)
        if endpoint.endswith("/"):
            # add trailing slash back
            url_path += "/"

    raw_data = await _call(urlunparse(url._replace(path=url_path)),
                           params, session=session)
    data = from_json(raw_data)
    if not data:
        raise EmptyResponse

    return data
