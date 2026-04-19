# SPDX-License-Identifier: EUPL-1.2
# SPDX-FileCopyrightText: 2026 Anna <cyber@sysrq.in>

from repology_client.types import CPE


def test_cpe_to_str():
    data = {
        "cpe_vendor": "alsa-project",
        "cpe_product": "alsa-plugins",
        "cpe_edition": "*", "cpe_lang": "*", "cpe_other": "*",
        "cpe_sw_edition": "*", "cpe_target_hw": "*", "cpe_target_sw": "*",
    }
    expected = "cpe:2.3:a:alsa-project:alsa-plugins:*:*:*:*:*:*:*:*"
    assert str(CPE.model_validate(data)) == expected


def test_cpe_to_str_incomplete():
    data = {
        "cpe_vendor": "alsa-project",
        "cpe_product": "alsa-plugins",
    }
    expected = "cpe:2.3:a:alsa-project:alsa-plugins:*:*:*:*:*:*:*:*"
    assert str(CPE.model_validate(data)) == expected
