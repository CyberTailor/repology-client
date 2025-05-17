.. SPDX-FileCopyrightText: 2024-2025 Anna <cyber@sysrq.in>
.. SPDX-License-Identifier: CC0-1.0

Release Notes
=============

0.3.0-next
----------

- **Breaking**: Remove experimental API endpoints, since there are no plans to
  re-implement them in the new Repology webapp.

- **New**: :py:func:`repology_client.get_problems` function for
  ``/api/v1/repository/<repo>/problems`` and
  ``/api/v1/maintainer/<maint>/problems-for-repo/<repo>`` endpoints.

0.3.0
-----

- **Breaking**: Switch types from Pydantic dataclasses to Pydantic models.

- Use ``collections.abc`` types in return annotations (such as ``Set`` and
  ``Mapping``).

- Initiate ``TypeAdapter`` once to improve perfomance.

- Defer building Pydantic models until the first use.

0.2.0
-----

- **New**: :py:func:`repology_client.exp.distromap` function for
  ``/api/experimental/distromap`` endpoint.

- Parse JSON with possibly faster Pydantic parser, since we already use this
  library.

- Improve API documentation and switch to Alabaster HTML theme.

0.1.0
-----

- **New:** :py:func:`repology_client.resolve_package` function providing
  `Project by package name`__ tool's functionality.

- **Gone:** Python 3.10 support.

- Fix default session not closing properly.

__ https://repology.org/tools/project-by

0.0.2
-----

- Fix fetching >200 projects.

0.0.1
-----

- First release
