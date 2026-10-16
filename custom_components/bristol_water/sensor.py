"""Sensors for Bristol Water."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType

from .coordinator import BristolWaterConfigEntry
from .entity import BristolWaterEntity

PARALLEL_UPDATES = 0

MEASUREMENTS = (
    "alkalinity_caco3",
    "alkalinity_hco3",
    "calcium",
    "chloride",
    "fluoride",
    "hardness",
    "magnesium",
    "nitrate",
    "phosphate",
    "sodium",
    "sulphate",
)

SENSORS: tuple[SensorEntityDescription, ...] = (
    *(
        SensorEntityDescription(
            key=key,
            translation_key=key,
            native_unit_of_measurement="mg/L",
            state_class=SensorStateClass.MEASUREMENT,
        )
        for key in MEASUREMENTS
    ),
    SensorEntityDescription(key="classification", translation_key="classification"),
    SensorEntityDescription(key="source", translation_key="source"),
    SensorEntityDescription(key="supply_zone", translation_key="supply_zone"),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BristolWaterConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the sensors."""
    async_add_entities(
        BristolWaterSensorEntity(entry.runtime_data, entry, description)
        for description in SENSORS
    )


class BristolWaterSensorEntity(BristolWaterEntity):
    """A Bristol Water quality sensor."""

    @property
    def native_value(self) -> StateType:
        """Return the sensor state."""
        return self.coordinator.data[self.entity_description.key]
