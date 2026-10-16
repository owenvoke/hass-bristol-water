"""Client for the Bristol Water water quality API."""

from __future__ import annotations

import asyncio
import re
from typing import Any, TypedDict

import httpx
from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import get_async_client

from .const import (
    API_ENDPOINT,
    DATA_KEY_ALKALINITY_CACO3,
    DATA_KEY_ALKALINITY_HCO3,
    DATA_KEY_CALCIUM,
    DATA_KEY_CHLORIDE,
    DATA_KEY_CLASSIFICATION,
    DATA_KEY_FLUORIDE,
    DATA_KEY_HARDNESS,
    DATA_KEY_MAGNESIUM,
    DATA_KEY_NITRATE,
    DATA_KEY_PHOSPHATE,
    DATA_KEY_SODIUM,
    DATA_KEY_SOURCE,
    DATA_KEY_SULPHATE,
    DATA_KEY_SUPPLY_ZONE,
)
from .util import parse_json_attributes

REQUEST_TIMEOUT = 10

DATA_KEYS = [
    DATA_KEY_SUPPLY_ZONE,
    DATA_KEY_SOURCE,
    DATA_KEY_CLASSIFICATION,
    DATA_KEY_CALCIUM,
    DATA_KEY_MAGNESIUM,
    DATA_KEY_HARDNESS,
    DATA_KEY_FLUORIDE,
    DATA_KEY_ALKALINITY_CACO3,
    DATA_KEY_ALKALINITY_HCO3,
    DATA_KEY_CHLORIDE,
    DATA_KEY_NITRATE,
    DATA_KEY_PHOSPHATE,
    DATA_KEY_SODIUM,
    DATA_KEY_SULPHATE,
]


class BristolWaterError(Exception):
    """The Bristol Water API could not be reached or returned an error."""


class NoDataError(BristolWaterError):
    """There is no water quality data for the postcode."""


class BristolWaterData(TypedDict):
    """Model for Bristol Water data."""

    alkalinity_caco3: str
    alkalinity_hco3: str
    calcium: str
    chloride: str
    classification: str | None
    fluoride: str
    hardness: str
    magnesium: str
    nitrate: str
    phosphate: str
    sodium: str
    source: str | None
    sulphate: str
    supply_zone: str


def format_classification(classification: str) -> str | None:
    match = re.search(
        r"Your drinking water supply is classed as\s+(?P<classification>.*?)\.",
        classification,
    )

    return match.group("classification") if match else None


def format_source(source: str) -> str | None:
    match = re.search(
        r"Your water supply comes from (?P<source>.+)",
        source,
    )

    return match.group("source") if match else None


def dict_from_api(data: dict[str, Any]) -> BristolWaterData:
    """Initialize from the API."""

    return BristolWaterData(
        alkalinity_caco3=data[DATA_KEY_ALKALINITY_CACO3],
        alkalinity_hco3=data[DATA_KEY_ALKALINITY_HCO3],
        calcium=data[DATA_KEY_CALCIUM],
        chloride=data[DATA_KEY_CHLORIDE],
        classification=format_classification(data[DATA_KEY_CLASSIFICATION]),
        fluoride=data[DATA_KEY_FLUORIDE],
        hardness=data[DATA_KEY_HARDNESS],
        magnesium=data[DATA_KEY_MAGNESIUM],
        nitrate=data[DATA_KEY_NITRATE],
        phosphate=data[DATA_KEY_PHOSPHATE],
        sodium=data[DATA_KEY_SODIUM],
        source=format_source(data[DATA_KEY_SOURCE]),
        sulphate=data[DATA_KEY_SULPHATE],
        supply_zone=data[DATA_KEY_SUPPLY_ZONE],
    )


async def get_data_for_postcode(hass: HomeAssistant, postcode: str) -> BristolWaterData:
    """Fetch the water quality data for a postcode."""
    try:
        async with asyncio.timeout(REQUEST_TIMEOUT):
            response = await get_async_client(hass).get(
                API_ENDPOINT, params={"q": postcode}
            )
            response.raise_for_status()
    except (httpx.HTTPError, TimeoutError) as err:
        raise BristolWaterError(str(err) or type(err).__name__) from err

    data = parse_json_attributes(response.text, DATA_KEYS, "$.objects[0].values")

    # Every key is needed to build the data.
    if not data or any(key not in data for key in DATA_KEYS):
        raise NoDataError(f"No water quality data found for {postcode}")

    return dict_from_api(data)
