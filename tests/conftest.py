"""Fixtures for Bristol Water tests."""

from __future__ import annotations

import json
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.bristol_water.const import CONF_POSTCODE, DOMAIN

VALUES = {
    "3": "Eastville, Easton, Netham and St Philips",
    "4": "Your water supply comes from surface water (lakes)",
    "5": "Your drinking water supply is classed as hard.  ",
    "6": 67,
    "7": 9.3,
    "8": "205",
    "13": "0.11",
    "14": "155",
    "15": "189",
    "16": "20",
    "17": "11",
    "18": "1.9",
    "19": "27",
    "20": "48",
}


def response(body: dict, status: int = 200) -> httpx.Response:
    return httpx.Response(
        status,
        text=json.dumps(body),
        request=httpx.Request("GET", "https://www.bristolwater.co.uk"),
    )


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Enable custom integrations in every test."""


@pytest.fixture
def mock_client() -> Generator[MagicMock]:
    """Patch the shared httpx client."""
    client = MagicMock()
    client.get = AsyncMock(return_value=response({"objects": [{"values": VALUES}]}))
    with patch(
        "custom_components.bristol_water.api.get_async_client", return_value=client
    ):
        yield client


@pytest.fixture
def config_entry() -> MockConfigEntry:
    """A configured Bristol Water entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="Bristol Water (BS1 4DJ)",
        unique_id="bristol_water_BS1 4DJ",
        data={CONF_POSTCODE: "BS1 4DJ"},
    )
