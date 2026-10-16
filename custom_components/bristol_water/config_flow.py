"""Config flow for the Bristol Water integration."""

from __future__ import annotations

import logging
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlowWithReload,
)
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import callback

from .api import BristolWaterError, NoDataError, get_data_for_postcode
from .const import CONF_POSTCODE, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

USER_SCHEMA = vol.Schema({vol.Required(CONF_POSTCODE): cv.string})

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=1)
        ),
    }
)


class BristolWaterConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Bristol Water."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Ask for a postcode."""
        errors: dict[str, str] = {}
        if user_input is not None:
            postcode = user_input[CONF_POSTCODE]
            await self.async_set_unique_id(f"bristol_water_{postcode}")
            self._abort_if_unique_id_configured()

            try:
                await get_data_for_postcode(self.hass, postcode)
            except NoDataError:
                errors[CONF_POSTCODE] = "invalid_postcode"
            except BristolWaterError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error fetching Bristol Water data")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=f"Bristol Water ({postcode})", data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(USER_SCHEMA, user_input),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> BristolWaterOptionsFlow:
        """Return the options flow."""
        return BristolWaterOptionsFlow()


class BristolWaterOptionsFlow(OptionsFlowWithReload):
    """Options for Bristol Water."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.config_entry.options
            ),
        )
