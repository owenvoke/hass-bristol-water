from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, ENTITY_ID_FORMAT
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import BristolWaterUpdateCoordinator, DOMAIN, CONF_POSTCODE


class BristolWaterEntity(
    CoordinatorEntity[BristolWaterUpdateCoordinator], SensorEntity
):
    """Representation of a Bristol Water sensor."""

    entity_description: SensorEntityDescription

    _entity_id_format = ENTITY_ID_FORMAT

    def __init__(
        self,
        coordinator: BristolWaterUpdateCoordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
    ):
        """Initialize the sensor and set the update coordinator."""
        super().__init__(coordinator)
        self._attr_name = description.name
        self._attr_unique_id = f"{entry.data[CONF_POSTCODE]}_{description.key}"

        self.entry = entry
        self.entity_description = description

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            name=self.coordinator.name,
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, f"{self.entry.entry_id}")},
            manufacturer="Bristol Water",
        )
