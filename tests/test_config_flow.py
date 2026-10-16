"""Tests for the Bristol Water config and options flows."""

from __future__ import annotations

from unittest.mock import MagicMock

import httpx
import pytest
from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.bristol_water.const import CONF_POSTCODE, DOMAIN

from .conftest import response


async def test_user_flow(hass: HomeAssistant, mock_client: MagicMock) -> None:
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_POSTCODE: "BS1 4DJ"}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Bristol Water (BS1 4DJ)"
    assert mock_client.get.call_args.kwargs["params"] == {"q": "BS1 4DJ"}


@pytest.mark.parametrize(
    ("return_value", "side_effect", "errors"),
    [
        (response({"objects": []}), None, {CONF_POSTCODE: "invalid_postcode"}),
        (response({}, status=500), None, {"base": "cannot_connect"}),
        (None, httpx.ConnectError("down"), {"base": "cannot_connect"}),
        (None, ValueError(), {"base": "unknown"}),
    ],
)
async def test_user_flow_errors(
    hass: HomeAssistant,
    mock_client: MagicMock,
    return_value: httpx.Response | None,
    side_effect: Exception | None,
    errors: dict[str, str],
) -> None:
    mock_client.get.return_value = return_value
    mock_client.get.side_effect = side_effect
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_POSTCODE: "XX1 1XX"}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == errors


async def test_options_flow_reloads(
    hass: HomeAssistant, mock_client: MagicMock, config_entry: MockConfigEntry
) -> None:
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {CONF_SCAN_INTERVAL: 12}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert config_entry.runtime_data.update_interval.total_seconds() == 12 * 3600
