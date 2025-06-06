import logging
from datetime import timedelta, datetime

from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from . import BristolWaterUpdateCoordinator
from .entity import BristolWaterEntity
from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

SCAN_INTERVAL = timedelta(hours=DEFAULT_SCAN_INTERVAL)


class BristolWaterSensorEntityDescription(SensorEntityDescription):
    """Class describing Bristol Water sensor entities."""


SENSORS: tuple[BristolWaterSensorEntityDescription, ...] = (
    BristolWaterSensorEntityDescription(
        key="alkalinity_caco3",
        name="Alkalinity (CaCO3)",
        native_unit_of_measurement="mg/L",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    BristolWaterSensorEntityDescription(
        key="alkalinity_hco3",
        name="Alkalinity (HCO3)",
        native_unit_of_measurement="mg/L",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    BristolWaterSensorEntityDescription(
        key="calcium",
        name="Calcium",
        native_unit_of_measurement="mg/L",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    BristolWaterSensorEntityDescription(
        key="chloride",
        name="Chloride",
        native_unit_of_measurement="mg/L",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    BristolWaterSensorEntityDescription(
        key="classification",
        name="Classification",
    ),
    BristolWaterSensorEntityDescription(
        key="fluoride",
        name="Fluoride",
        native_unit_of_measurement="mg/L",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    BristolWaterSensorEntityDescription(
        key="hardness",
        name="Hardness",
        native_unit_of_measurement="mg/L",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    BristolWaterSensorEntityDescription(
        key="magnesium",
        name="Magnesium",
        native_unit_of_measurement="mg/L",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    BristolWaterSensorEntityDescription(
        key="nitrate",
        name="Nitrate",
        native_unit_of_measurement="mg/L",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    BristolWaterSensorEntityDescription(
        key="phosphate",
        name="Phosphate",
        native_unit_of_measurement="mg/L",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    BristolWaterSensorEntityDescription(
        key="sodium",
        name="Sodium",
        native_unit_of_measurement="mg/L",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    BristolWaterSensorEntityDescription(
        key="source",
        name="Source",
    ),
    BristolWaterSensorEntityDescription(
        key="sulphate",
        name="Sulphate",
        native_unit_of_measurement="mg/L",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:water",
    ),
    BristolWaterSensorEntityDescription(
        key="supply_zone", name="Supply Zone", icon="mdi:map"
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up all sensors for this entry."""
    coordinator: BristolWaterUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        BristolWaterSensorEntity(coordinator, entry, description)
        for description in SENSORS
    )


class BristolWaterSensorEntity(BristolWaterEntity, SensorEntity):
    """Representation of a Bristol Water sensor."""

    entity_description: BristolWaterSensorEntityDescription

    @property
    def native_value(self) -> StateType | datetime:
        """Return the sensor state."""
        return self.coordinator.data[self.entity_description.key]
