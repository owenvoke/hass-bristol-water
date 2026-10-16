"""Tests for Bristol Water setup and sensors."""

from __future__ import annotations

from unittest.mock import MagicMock

import httpx
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry


async def test_sensors(
    hass: HomeAssistant, mock_client: MagicMock, config_entry: MockConfigEntry
) -> None:
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    prefix = "sensor.bristol_water_bs1_4dj"
    hardness = hass.states.get(f"{prefix}_hardness")
    assert hardness.state == "205"
    assert hardness.attributes["unit_of_measurement"] == "mg/L"
    assert hass.states.get(f"{prefix}_classification").state == "hard"
    assert hass.states.get(f"{prefix}_source").state == "surface water (lakes)"
    assert hass.states.get(f"{prefix}_supply_zone").state.startswith("Eastville")


async def test_setup_retries_on_network_error(
    hass: HomeAssistant, mock_client: MagicMock, config_entry: MockConfigEntry
) -> None:
    mock_client.get.side_effect = httpx.ConnectError("down")
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    assert config_entry.state is ConfigEntryState.SETUP_RETRY
