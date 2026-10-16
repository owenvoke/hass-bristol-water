"""Data update coordinator for Bristol Water."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import BristolWaterData, BristolWaterError, get_data_for_postcode
from .const import CONF_POSTCODE, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

type BristolWaterConfigEntry = ConfigEntry[BristolWaterUpdateCoordinator]


class BristolWaterUpdateCoordinator(DataUpdateCoordinator[BristolWaterData]):
    """Fetch the water quality for a postcode."""

    config_entry: BristolWaterConfigEntry

    def __init__(
        self, hass: HomeAssistant, config_entry: BristolWaterConfigEntry
    ) -> None:
        """Initialise the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(
                hours=int(
                    config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                )
            ),
        )
        self._postcode: str = config_entry.data[CONF_POSTCODE]

    async def _async_update_data(self) -> BristolWaterData:
        """Fetch the latest water quality data."""
        try:
            return await get_data_for_postcode(self.hass, self._postcode)
        except BristolWaterError as err:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_failed",
                translation_placeholders={"error": str(err)},
            ) from err
