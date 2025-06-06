"""Constants for the Bristol Water integration."""

from typing import Final

DOMAIN: Final = "bristol_water"

DEFAULT_SCAN_INTERVAL: Final = 24

CONF_POSTCODE: Final = "postcode"

API_ENDPOINT: Final = "https://www.bristolwater.co.uk/_hcms/api/getWQHubdbDataInfo"

DATA_KEY_SUPPLY_ZONE: Final = "3"
DATA_KEY_SOURCE: Final = "4"
DATA_KEY_CLASSIFICATION: Final = "5"
DATA_KEY_CALCIUM: Final = "6"
DATA_KEY_MAGNESIUM: Final = "7"
DATA_KEY_HARDNESS: Final = "8"
DATA_KEY_FLUORIDE: Final = "13"
DATA_KEY_ALKALINITY_CACO3: Final = "14"
DATA_KEY_ALKALINITY_HCO3: Final = "15"
DATA_KEY_CHLORIDE: Final = "16"
DATA_KEY_NITRATE: Final = "17"
DATA_KEY_PHOSPHATE: Final = "18"
DATA_KEY_SODIUM: Final = "19"
DATA_KEY_SULPHATE: Final = "20"
