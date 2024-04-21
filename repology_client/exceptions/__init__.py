# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2024 Anna <cyber@sysrq.in>

""" Exceptions this library can raise. """


class RepologyException(Exception):
    """
    Base class for all our exceptions. Pinkie promise.
    """


class InvalidInput(RepologyException):
    """
    A function was given invalid parameters.
    """


class EmptyResponse(RepologyException):
    """
    Raised if API returned empty object. Is it an error or everything's correct,
    just nothing matched your search criteria? Who knows.
    """
