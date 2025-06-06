import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.bristol_water.api import BristolWaterData, get_data_for_postcode

_LOGGER = logging.getLogger(__name__)


class BristolWaterUpdateCoordinator(DataUpdateCoordinator[BristolWaterData]):
    """Coordinates updates between all Bristol Water sensors defined."""

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        postcode: str,
        update_interval: timedelta,
    ) -> None:
        self._postcode = postcode

        """Initialize the UpdateCoordinator for Bristol Water sensors."""
        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> BristolWaterData:
        return await get_data_for_postcode(self.hass, self._postcode)
