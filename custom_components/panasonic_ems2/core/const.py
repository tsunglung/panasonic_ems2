"""Constants of the Panasonic Smart Home component."""

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription
)

from homeassistant.components.number import (
    NumberEntityDescription
)

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass
)

from homeassistant.components.select import (
    SelectEntityDescription
)

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntityDescription
)

from homeassistant.components.climate.const import (
    HVACMode,
    PRESET_BOOST,
    PRESET_ECO,
    PRESET_COMFORT,
    PRESET_SLEEP,
    PRESET_ACTIVITY,
    SWING_ON,
    SWING_OFF,
    SWING_BOTH,
    SWING_VERTICAL,
    SWING_HORIZONTAL
)
from homeassistant.const import (
    EntityCategory,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfMass,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume
)

DOMAIN = "panasonic_ems2"

DOMAINS = [
    "binary_sensor",
    "climate",
    "fan",
    "humidifier",
    "number",
    "sensor",
    "select",
    "switch"
]

HA_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
BASE_URL = 'https://ems2.panasonic.com.tw/api'
APP_TOKEN = "D8CBFF4C-2824-4342-B22D-189166FEF503"

DATA_CLIENT = "client"
DATA_COORDINATOR = "coordinator"

CONF_UPDATE_INTERVAL = "update_interval"
CONF_CPTOKEN = "cptoken"
CONF_TOKEN_TIMEOUT = "cptoken_timeout"
CONF_REFRESH_TOKEN = "refresh_token"
CONF_REFRESH_TOKEN_TIMEOUT = "refresh_token_timeout"

DEFAULT_UPDATE_INTERVAL = 120
REQUEST_TIMEOUT = 15

DATA_CLIENT = "client"
DATA_COORDINATOR = "coordinator"
UPDATE_LISTENER = "update_listener"

USER_INFO_TYPES = [
#    "Power",
#    "Temp",
#    "Humid",
#    "PM",
    "Other"
]

ENTITY_MONTHLY_ENERGY = "0xA0"
ENTITY_DOOR_OPENS = "0xA1"
ENTITY_WATER_USED = "0xA2"
ENTITY_WASH_TIMES = "0xA3"
ENTITY_UPDATE = "0xB0"
ENTITY_UPDATE_INFO = "0xB1"
ENTITY_EMPTY = "0xFF"

DEVICE_TYPE_CLIMATE = 1
DEVICE_TYPE_FRIDGE = 2
DEVICE_TYPE_WASHING_MACHINE = 3
DEVICE_TYPE_DEHUMIDIFIER = 4
DEVICE_TYPE_AIRPURIFIER = 8
DEVICE_TYPE_ERV = 14
DEVICE_TYPE_FAN = 15
DEVICE_TYPE_WEIGHT_PLATE = 23

AIRPURIFIER_OPERATING_MODE = "0x01"
AIRPURIFIER_TIMER_ON = "0x02"
AIRPURIFIER_TIMER_OFF = "0x03"
AIRPURIFIER_AIR_QUALITY = "0x04"
AIRPURIFIER_RESET_FILTER_NOTIFY = "0x05"
AIRPURIFIER_NANOEX = "0x07"
AIRPURIFIER_BUZZER = "0x08"
AIRPURIFIER_PM25 = "0x61"
AIRPURIFIER_LIGHT = "0x62"
AIRPURIFIER_RUNNING_TIME = "0x63"
AIRPURIFIER_RESERVED = "0x7F"

AIRPURIFIER_NANOEX_PRESET = "nanoe™ X"
AIRPURIFIER_PRESET_MODES = {
    AIRPURIFIER_NANOEX: AIRPURIFIER_NANOEX_PRESET,
}

CLIMATE_AVAILABLE_MODES = {
    HVACMode.COOL: 0,
    HVACMode.DRY: 1,
    HVACMode.FAN_ONLY: 2,
    HVACMode.AUTO: 3,
    HVACMode.HEAT: 4
}

CLIMATE_AVAILABLE_SWING_MODES = [
    SWING_ON,
    SWING_OFF,
    SWING_BOTH,
    SWING_VERTICAL,
    SWING_HORIZONTAL
]
CLIMATE_AVAILABLE_FAN_MODES = {
    "Auto": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "11": 11,
    "12": 12,
    "13": 13,
    "14": 14,
    "15": 15
}
CLIMATE_MINIMUM_TEMPERATURE = 16
CLIMATE_MAXIMUM_TEMPERATURE = 30
CLIMATE_TEMPERATURE_STEP = 1.0
CLIMATE_ON_TIMER_MIN = 0
CLIMATE_ON_TIMER_MAX = 1440
CLIMATE_OFF_TIMER_MIN = 0
CLIMATE_OFF_TIMER_MAX = 1440

CLIMATE_POWER = "0x00"
CLIMATE_OPERATING_MODE = "0x01"
CLIMATE_FAN_SPEED = "0x02"
CLIMATE_TARGET_TEMPERATURE = "0x03"
CLIMATE_TEMPERATURE_INDOOR = "0x04"
CLIMATE_SLEEP_MODE = "0x05"
CLIMATE_FUZZY_MODE = "0x07"
CLIMATE_AIRFRESH_MODE = "0x08"
CLIMATE_TIMER_ON = "0x0B"
CLIMATE_TIMER_OFF = "0x0C"
CLIMATE_SWING_VERTICAL = "0x0E"
CLIMATE_SWING_VERTICAL_LEVEL = "0x0F"
CLIMATE_SWING_HORIZONTAL = "0x10"
CLIMATE_SWING_HORIZONTAL_LEVEL = "0x11"
CLIMATE_SET_HUMIDITY = "0x13"
CLIMATE_HUMIDITY_INDOOR = "0x14"
CLIMATE_ERROR_CODE = "0x15"
CLIMATE_ANTI_MILDEW = "0x17"
CLIMATE_AUTO_CLEAN = "0x18"
CLIMATE_ACTIVITY = "0x19"
CLIMATE_BOOST = "0x1A"
CLIMATE_ECO = "0x1B"
CLIMATE_COMFORT = "0x1C"
CLIMATE_BUZZER = "0x1E"
CLIMATE_INDICATOR_LIGHT = "0x1F"
CLIMATE_TEMPERATURE_OUTDOOR = "0x21"
CLIMATE_OPERATING_POWER = "0x27"
CLIMATE_ENERGY = "0x28"
CLIMATE_PM25 = "0x37"
CLIMATE_MONITOR_MILDEW = "0x53"
CLIMATE_61 = "0x61"
CLIMATE_RESERVED = "0x7F"
CLIMATE_PRESET_MODE = "0x80"
CLIMATE_SWING_MODE = "0x81"

CLIMATE_AVAILABLE_PRESET_MODES = {
    CLIMATE_ACTIVITY: PRESET_ACTIVITY,
    CLIMATE_BOOST: PRESET_BOOST,
    CLIMATE_COMFORT: PRESET_COMFORT,
    CLIMATE_ECO: PRESET_ECO,
    CLIMATE_SLEEP_MODE: PRESET_SLEEP
}

CLIMATE_RX_COMMANDS = [
                CLIMATE_ERROR_CODE,
                CLIMATE_OPERATING_POWER,
                CLIMATE_PM25,
                CLIMATE_61
            ]
CLIMATE_PXGD_COMMMANDS = []
CLIMATE_PXGD_MODELS = [
    "J-DUCT", "SX-DUCT", "GX", "LJ", "LX", "PX", "QX", "LJV", "PXGD" "RX-N"
]

CLIMATE_PM10_MODELS = [
    "JHW"
]

CLIMATE_PM10_2_MODELS = [
    "JHV2"
]

CLIMATE_PM25_MODELS = [
    "EHW", "GHW", "JHW", "JHV2"
]

DEHUMIDIFIER_POWER = "0x00"
DEHUMIDIFIER_MODE = "0x01"
DEHUMIDIFIER_TIMER_OFF = "0x02"
DEHUMIDIFIER_RELATIVE_HUMIDITY = "0x03"
DEHUMIDIFIER_TARGET_HUMIDITY = "0x04"
DEHUMIDIFIER_HUMIDITY_INDOOR = "0x07"
DEHUMIDIFIER_FAN_SPEED = "0x09"
DEHUMIDIFIER_WATER_TANK_STATUS = "0x0A"
DEHUMIDIFIER_FILTER_CLEAN = "0x0B"
DEHUMIDIFIER_AIRFRESH_MODE = "0x0D"
DEHUMIDIFIER_FAN_MODE = "0x0E"
DEHUMIDIFIER_ERROR_CODE = "0x12"
DEHUMIDIFIER_BUZZER = "0x18"
DEHUMIDIFIER_ENERGY = "0x1D"
DEHUMIDIFIER_50 = "0x50"
DEHUMIDIFIER_51 = "0x51"
DEHUMIDIFIER_PM25 = "0x53"
DEHUMIDIFIER_TIMER_ON = "0x55"
DEHUMIDIFIER_PM10 = "0x56"
DEHUMIDIFIER_58 = "0x58"
DEHUMIDIFIER_59 = "0x59"

DEHUMIDIFIER_MAX_HUMIDITY = 70
DEHUMIDIFIER_MIN_HUMIDITY = 40

DEHUMIDIFIER_DEFAULT_MODES = {
    "Auto": 0,
    "Set": 1,
    "Continuous": 2,
    "Cloth Dry": 3
}

DEHUMIDIFIER_PERFORMANCE_MODELS = ["KBS", "LMS", "NM"]

DEHUMIDIFIER_GHW_COMMANDS = []

DEHUMIDIFIER_JHW_COMMANDS = [
    DEHUMIDIFIER_ERROR_CODE,
#    DEHUMIDIFIER_51,
    DEHUMIDIFIER_PM25,
    DEHUMIDIFIER_PM10,
    DEHUMIDIFIER_58,
#    DEHUMIDIFIER_59
]

ERV_POWER = "0x00"
ERV_OPERATING_MODE = "0x01"
ERV_FAN_SPEED = "0x02"
ERV_TARGET_TEMPERATURE = "0x03"
ERV_TEMPERATURE_IN = "0x04"
ERV_TEMPERATURE_OUT = "0x05"
ERV_TIMER_ON = "0x06"
ERV_ERROR_CODE = "0x09"
ERV_ENERGY = "0x0E"
ERV_RESET_FILTER_NOTIFY = "0x14"
ERV_VENTILATE_MODE = "0x15"
ERV_PRE_HEAT_COOL = "0x16"
ERV_REVERED = "0x7F"

ERV_MINIMUM_TEMPERATURE = -128
ERV_MAXIMUM_TEMPERATURE = 127

ERV_AVAILABLE_MODES = {
    "Cool": 0,
    "Dehumidify": 1,
    "Fan": 2,
    "Auto": 3,
    "Heat": 4
}
ERV_AVAILABLE_FAN_MODES = {
    "Auto": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "11": 11,
    "12": 12,
    "13": 13,
    "14": 14,
    "15": 15
}

FAN_POWER = "0x00"
FAN_OPERATING_MODE = "0x01"
FAN_SPEED = "0x02"
FAN_TEMPERATURE_INDOOR = "0x03"
FAN_OSCILLATE = "0x05"

FAN_PRESET_MODES = {
    "mode 1": 0,
    "mode 2": 1,
    "mode 3": 2,
    "mode 4": 3,
    "mode 5": 4
}

FRIDGE_FREEZER_MODE = "0x00"
FRIDGE_CHAMBER_MODE = "0x01"
FRIDGE_FREEZER_TEMPERATURE = "0x03"
FRIDGE_CHAMBER_TEMPERATURE = "0x05"
FRIDGE_ECO = "0x0C"
FRIDGE_ERROR_CODE = "0x0E"
FRIDGE_ENERGY = "0x13"
FRIDGE_DEFROST_SETTING = "0x50"
FRIDGE_STOP_ICE_MAKING = "0x52"
FRIDGE_FAST_ICE_MAKING = "0x53"
FRIDGE_FRESH_QUICK_FREZZE = "0x56"
FRIDGE_THAW_MODE = "0x57"
FRIDGE_THAW_TEMPERATURE = "0x58"
FRIDGE_WINTER_MDOE = "0x5A"
FRIDGE_SHOPPING_MODE = "0x5B"
FRIDGE_GO_OUT_MODE = "0x5C"
FRIDGE_NANOEX = "0x61"
FRIDGE_ERROR_CODE_JP = "0x63"

FRIDGE_XGS_COMMANDS = [
                FRIDGE_ECO,
                FRIDGE_FREEZER_TEMPERATURE,
                FRIDGE_CHAMBER_TEMPERATURE,
                FRIDGE_THAW_TEMPERATURE,
                FRIDGE_ENERGY,
                FRIDGE_NANOEX
            ]

FRIDGE_MODELS = [
    "NR-F655WX-X1", "NR-F655WX-X", "NR-F655WPX"
]

FRIDGE_2020_MODELS = [
    "NR-F506HX-N1", "NR-F506HX-W1", "NR-F506HX-X1", "NR-F556HX-N1",
    "NR-F556HX-W1", "NR-F556HX-X1", "NR-F606HX-N1", "NR-F606HX-W1",
    "NR-F606HX-X1", "NR-F656WX-X1"
]

WASHING_MACHINE_POWER = "0x00"
WASHING_MACHINE_ENABLE = "0x01"
WASHING_MACHINE_PROGRESS = "0x02"
WASHING_MACHINE_OPERATING_STATUS_OLD = "0x03"
WASHING_MACHINE_REMAING_WASH_TIME= "0x13"
WASHING_MACHINE_TIMER = "0x14"
WASHING_MACHINE_TIMER_REMAINING_TIME_OLD = "0x15"
WASHING_MACHINE_ERROR_CODE = "0x19"
WASHING_MACHINE_ENERGY = "0x1E"
WASHING_MACHINE_OPERATING_STATUS = "0x50"
WASHING_MACHINE_51 = "0x51"
WASHING_MACHINE_52 = "0x52"
WASHING_MACHINE_53 = "0x53"
WASHING_MACHINE_CURRENT_MODE = "0x54"
WASHING_MACHINE_CURRENT_PROGRESS = "0x55"
WASHING_MACHINE_POSTPONE_DRYING = "0x56"
WASHING_MACHINE_57 = "0x57"
WASHING_MACHINE_TIMER_REMAINING_TIME = "0x58"
WASHING_MACHINE_59 = "0x59"
WASHING_MACHINE_60 = "0x60"
WASHING_MACHINE_61 = "0x61"
WASHING_MACHINE_PROGRESS_NEW = "0x64"
WASHING_MACHINE_66 = "0x66"
WASHING_MACHINE_67 = "0x67"
WASHING_MACHINE_68 = "0x68"
WASHING_MACHINE_WARM_WATER = "0x69"
WASHING_MACHINE_71 = "0x71"
WASHING_MACHINE_72 = "0x72"
WASHING_MACHINE_73 = "0x73"
WASHING_MACHINE_REMOTE_CONTROL = "0x74"

WASHING_MACHINE_MODELS = ["DDH", "DW","HDH", "MDH"]
WASHING_MACHINE_2020_MODELS = ["KBS", "LM", "LMS"]

WASHING_MACHINE_LX128B_COMMANDS = [
    WASHING_MACHINE_71,
    WASHING_MACHINE_72,
    WASHING_MACHINE_73
]

WASHING_MACHINE_HDH_COMMANDS = [
    WASHING_MACHINE_OPERATING_STATUS_OLD,
    WASHING_MACHINE_TIMER_REMAINING_TIME_OLD,
    WASHING_MACHINE_53,
    WASHING_MACHINE_57,
#    WASHING_MACHINE_68
]

WASHING_MACHINE_KBS_COMMANDS = [
    WASHING_MACHINE_TIMER_REMAINING_TIME_OLD
]

WEIGHT_PLATE_GET_WEIGHT = "0x52"
WEIGHT_PLATE_FOOD_NAME = "0x80"
WEIGHT_PLATE_MANAGEMENT_MODE = "0x81"
WEIGHT_PLATE_MANAGEMENT_VALUE = "0x82"
WEIGHT_PLATE_AMOUNT_MAX = "0x83"
WEIGHT_PLATE_BUY_DATE = "0x84"
WEIGHT_PLATE_DUE_DATE = "0x85"
WEIGHT_PLATE_COMMUNICATION_MODE = "0x8A"
WEIGHT_PLATE_COMMUNICATION_TIME = "0x8B"
WEIGHT_PLATE_TOTAL_WEIGHT = "0x8C"
WEIGHT_PLATE_RESTORE_WEIGHT = "0x8D"
WEIGHT_PLATE_LOW_BATTERY = "0x8E"

MODEL_JP_TYPES = [
    "F655",
    "F656",
    "F657",
    "F658",
    "F659",
    "LX128B"
]

COMMANDS_TYPE= {
    str(DEVICE_TYPE_AIRPURIFIER): [
        AIRPURIFIER_OPERATING_MODE,
        AIRPURIFIER_TIMER_ON,
        AIRPURIFIER_TIMER_OFF,
        AIRPURIFIER_AIR_QUALITY,
        AIRPURIFIER_NANOEX,
        AIRPURIFIER_BUZZER,
        AIRPURIFIER_PM25,
        AIRPURIFIER_LIGHT
    ],
    str(DEVICE_TYPE_CLIMATE): [
        CLIMATE_POWER,
        CLIMATE_OPERATING_MODE,
        CLIMATE_FAN_SPEED,
        CLIMATE_TARGET_TEMPERATURE,
        CLIMATE_TEMPERATURE_INDOOR,
        CLIMATE_SLEEP_MODE,
        CLIMATE_AIRFRESH_MODE,
        CLIMATE_TIMER_ON,
        CLIMATE_TIMER_OFF,
        CLIMATE_SWING_VERTICAL_LEVEL,
        CLIMATE_SWING_HORIZONTAL_LEVEL,
        CLIMATE_ANTI_MILDEW,
        CLIMATE_AUTO_CLEAN,
        CLIMATE_ACTIVITY,
        CLIMATE_BOOST,
        CLIMATE_ECO,
        CLIMATE_BUZZER,
        CLIMATE_INDICATOR_LIGHT,
        CLIMATE_ENERGY,
        CLIMATE_TEMPERATURE_OUTDOOR
    ],
    str(DEVICE_TYPE_DEHUMIDIFIER): [
        DEHUMIDIFIER_POWER,
        DEHUMIDIFIER_MODE,
        DEHUMIDIFIER_TIMER_OFF,
        DEHUMIDIFIER_TARGET_HUMIDITY,
        DEHUMIDIFIER_HUMIDITY_INDOOR,
        DEHUMIDIFIER_FAN_SPEED,
        DEHUMIDIFIER_WATER_TANK_STATUS,
        DEHUMIDIFIER_AIRFRESH_MODE,
        DEHUMIDIFIER_FAN_MODE,
        DEHUMIDIFIER_BUZZER,
        DEHUMIDIFIER_ENERGY,
        DEHUMIDIFIER_50,
        DEHUMIDIFIER_TIMER_ON
    ],
    str(DEVICE_TYPE_ERV): [
        ERV_POWER,
        ERV_OPERATING_MODE,
        ERV_FAN_SPEED,
        ERV_TARGET_TEMPERATURE,
        ERV_TEMPERATURE_IN,
        ERV_TEMPERATURE_OUT,
        ERV_ERROR_CODE,
        ERV_ENERGY
    ],
    str(DEVICE_TYPE_FRIDGE): [
        FRIDGE_FREEZER_MODE,
        FRIDGE_CHAMBER_MODE,
        FRIDGE_DEFROST_SETTING,
        FRIDGE_STOP_ICE_MAKING,
        FRIDGE_FAST_ICE_MAKING,
        FRIDGE_FRESH_QUICK_FREZZE,
        FRIDGE_THAW_MODE,
        FRIDGE_WINTER_MDOE,
        FRIDGE_SHOPPING_MODE,
        FRIDGE_GO_OUT_MODE
    ],
    str(DEVICE_TYPE_WASHING_MACHINE): [
        WASHING_MACHINE_ENABLE,
        WASHING_MACHINE_REMAING_WASH_TIME,
        WASHING_MACHINE_TIMER,
        WASHING_MACHINE_ERROR_CODE,
        WASHING_MACHINE_TIMER_REMAINING_TIME,
        WASHING_MACHINE_ENERGY,
        WASHING_MACHINE_OPERATING_STATUS,
        WASHING_MACHINE_CURRENT_MODE,
        WASHING_MACHINE_CURRENT_PROGRESS,
        WASHING_MACHINE_POSTPONE_DRYING,
        WASHING_MACHINE_PROGRESS,
        WASHING_MACHINE_WARM_WATER,
        WASHING_MACHINE_52,
        WASHING_MACHINE_66,
        WASHING_MACHINE_67,
        WASHING_MACHINE_REMOTE_CONTROL
    ],
    str(DEVICE_TYPE_WEIGHT_PLATE): [
        WEIGHT_PLATE_GET_WEIGHT
    ]
}

EXTRA_COMMANDS = {
    str(DEVICE_TYPE_CLIMATE): {
        "RX-N": CLIMATE_RX_COMMANDS + [CLIMATE_MONITOR_MILDEW],
        "RX-G": CLIMATE_RX_COMMANDS,
        "RX-J": CLIMATE_RX_COMMANDS
    },
    str(DEVICE_TYPE_DEHUMIDIFIER): {
        "JHW": DEHUMIDIFIER_JHW_COMMANDS
    },
    str(DEVICE_TYPE_ERV): {
    },
    str(DEVICE_TYPE_FRIDGE): {
        "XGS": FRIDGE_XGS_COMMANDS,
        "F655": [FRIDGE_ERROR_CODE_JP],
        "F656": [FRIDGE_ERROR_CODE_JP],
        "F657": [FRIDGE_ERROR_CODE_JP],
        "F658": [FRIDGE_ERROR_CODE_JP],
        "F659": [FRIDGE_ERROR_CODE_JP]
    },
    str(DEVICE_TYPE_WASHING_MACHINE): {
        "LX128B": WASHING_MACHINE_LX128B_COMMANDS,
        "DDH": WASHING_MACHINE_HDH_COMMANDS,
        "DW": WASHING_MACHINE_HDH_COMMANDS,
        "HDH": WASHING_MACHINE_HDH_COMMANDS,
        "MDH": WASHING_MACHINE_HDH_COMMANDS,
        "KBS": WASHING_MACHINE_KBS_COMMANDS,
        "LM": WASHING_MACHINE_KBS_COMMANDS,
        "LMS": WASHING_MACHINE_KBS_COMMANDS
    },
    str(DEVICE_TYPE_AIRPURIFIER): {
    }
}

EXCESS_COMMANDS = {
    str(DEVICE_TYPE_CLIMATE): {
        "J-DUCT": [CLIMATE_SWING_VERTICAL_LEVEL, CLIMATE_SWING_HORIZONTAL_LEVEL],
    },
    str(DEVICE_TYPE_DEHUMIDIFIER): {
    },
    str(DEVICE_TYPE_ERV): {
    },
    str(DEVICE_TYPE_FRIDGE): {
    },
    str(DEVICE_TYPE_WASHING_MACHINE): {
    },
    str(DEVICE_TYPE_AIRPURIFIER): {
    }
}

SET_COMMAND_TYPE = {
    str(DEVICE_TYPE_CLIMATE): {
        CLIMATE_PRESET_MODE: 1,
        CLIMATE_TARGET_TEMPERATURE: 3,
        CLIMATE_SLEEP_MODE: 5,
        CLIMATE_ANTI_MILDEW: 23,
        CLIMATE_AUTO_CLEAN: 24,
        CLIMATE_BUZZER: 30,
        CLIMATE_POWER: 128,
        CLIMATE_OPERATING_MODE: 129,
        CLIMATE_FAN_SPEED: 130,
        CLIMATE_ECO: 136,
        CLIMATE_TIMER_ON: 139,
        CLIMATE_TIMER_OFF: 140,
        CLIMATE_SWING_MODE: 143,
        CLIMATE_ACTIVITY: 153,
        CLIMATE_BOOST: 154,
        CLIMATE_AUTO_CLEAN: 155,
        CLIMATE_INDICATOR_LIGHT: 159
    },
    str(DEVICE_TYPE_DEHUMIDIFIER): {
        DEHUMIDIFIER_POWER: 128,
        DEHUMIDIFIER_MODE: 129,
        DEHUMIDIFIER_TARGET_HUMIDITY: 132,
        DEHUMIDIFIER_FAN_SPEED: 137,
        DEHUMIDIFIER_AIRFRESH_MODE: 141,
        DEHUMIDIFIER_FAN_MODE: 142,
        DEHUMIDIFIER_BUZZER: 152,
        DEHUMIDIFIER_TIMER_ON: 213
    },
    str(DEVICE_TYPE_WASHING_MACHINE): {
        WASHING_MACHINE_ENABLE: 1,
        WASHING_MACHINE_TIMER: 20,
        WASHING_MACHINE_PROGRESS: 130,
        WASHING_MACHINE_PROGRESS_NEW: 100,
        WASHING_MACHINE_WARM_WATER: 105
    }
}


@dataclass
class PanasonicBinarySensorDescription(
    BinarySensorEntityDescription
):
    """Class to describe an Panasonic binary sensor."""
    options_value: list[str] | None = None


AIRPURIFIER_BINARY_SENSORS: tuple[PanasonicBinarySensorDescription, ...] = (
    PanasonicBinarySensorDescription(
        key=ENTITY_UPDATE,
        name="Firmware Update",
        icon='mdi:package-up',
        device_class=BinarySensorDeviceClass.UPDATE
    ),
    PanasonicBinarySensorDescription(
        key=ENTITY_EMPTY,
        name="Empty",
        icon="mdi:cog"
    )
)

CLIMATE_BINARY_SENSORS: tuple[PanasonicBinarySensorDescription, ...] = (
    PanasonicBinarySensorDescription(
        key=ENTITY_UPDATE,
        name="Firmware Update",
        icon='mdi:package-up',
        device_class=BinarySensorDeviceClass.UPDATE
    ),
    PanasonicBinarySensorDescription(
        key=ENTITY_EMPTY,
        name="Empty",
        icon='mdi:cog'
    )
)

DEHUMIDIFIER_BINARY_SENSORS: tuple[PanasonicBinarySensorDescription, ...] = (
    PanasonicBinarySensorDescription(
        key=ENTITY_UPDATE,
        name="Firmware Update",
        icon='mdi:package-up',
        device_class=BinarySensorDeviceClass.UPDATE
    ),
    PanasonicBinarySensorDescription(
        key=DEHUMIDIFIER_WATER_TANK_STATUS,
        name="Water Tank",
        icon='mdi:cup-water'
    )
)

ERV_BINARY_SENSORS: tuple[PanasonicBinarySensorDescription, ...] = (
    PanasonicBinarySensorDescription(
        key=ENTITY_UPDATE,
        name="Firmware Update",
        icon='mdi:package-up',
        device_class=BinarySensorDeviceClass.UPDATE
    ),
    PanasonicBinarySensorDescription(
        key=ENTITY_EMPTY,
        name="Empty",
        icon='mdi:cog'
    )
)

FRIDGE_BINARY_SENSORS: tuple[PanasonicBinarySensorDescription, ...] = (
    PanasonicBinarySensorDescription(
        key=ENTITY_UPDATE,
        name="Firmware Update",
        icon='mdi:package-up',
        device_class=BinarySensorDeviceClass.UPDATE
    ),
    PanasonicBinarySensorDescription(
        key=ENTITY_EMPTY,
        name="Empty",
        icon='mdi:cog'
    )
)

WASHING_MACHINE_BINARY_SENSORS: tuple[PanasonicBinarySensorDescription, ...] = (
    PanasonicBinarySensorDescription(
        key=ENTITY_UPDATE,
        name="Firmware Update",
        icon='mdi:package-up',
        device_class=BinarySensorDeviceClass.UPDATE
    ),
    PanasonicBinarySensorDescription(
        key=ENTITY_EMPTY,
        name="Empty",
        icon='mdi:cog'
    )
)

@dataclass
class PanasonicNumberDescription(
    NumberEntityDescription
):
    """Class to describe an Panasonic number."""
    options_value: list[str] | None = None


AIRPURIFIER_NUMBERS: tuple[PanasonicNumberDescription, ...] = (
    PanasonicNumberDescription(
        key=AIRPURIFIER_TIMER_ON,
        name="Timer On",
        native_unit_of_measurement=UnitOfTime.HOURS,
        entity_category=EntityCategory.CONFIG,
        icon='mdi:timer-cog-outline',
        native_min_value=0,
        native_max_value=24,
        native_step=1,
        entity_registry_enabled_default=False
    ),
    PanasonicNumberDescription(
        key=AIRPURIFIER_TIMER_OFF,
        name="Timer Off",
        native_unit_of_measurement=UnitOfTime.HOURS,
        entity_category=EntityCategory.CONFIG,
        icon='mdi:timer-cog',
        native_min_value=0,
        native_max_value=24,
        native_step=1,
        entity_registry_enabled_default=False
    )
)

CLIMATE_NUMBERS: tuple[PanasonicNumberDescription, ...] = (
    PanasonicNumberDescription(
        key=CLIMATE_TIMER_ON,
        name="Timer On",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        entity_category=EntityCategory.CONFIG,
        icon='mdi:timer-cog-outline',
        native_min_value=0,
        native_max_value=1440,
        native_step=1,
        entity_registry_enabled_default=False
    ),
    PanasonicNumberDescription(
        key=CLIMATE_TIMER_OFF,
        name="Timer Off",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        entity_category=EntityCategory.CONFIG,
        icon='mdi:timer-cog',
        native_min_value=0,
        native_max_value=1440,
        native_step=1,
        entity_registry_enabled_default=False
    )
)

DEHUMIDIFIER_NUMBERS: tuple[PanasonicNumberDescription, ...] = (
    PanasonicNumberDescription(
        key=DEHUMIDIFIER_TIMER_ON,
        name="Timer On",
        native_unit_of_measurement=UnitOfTime.HOURS,
        entity_category=EntityCategory.CONFIG,
        icon='mdi:timer-cog-outline',
        native_min_value=0,
        native_max_value=12,
        native_step=1,
        entity_registry_enabled_default=False
    ),
    PanasonicNumberDescription(
        key=DEHUMIDIFIER_TIMER_OFF,
        name="Timer Off",
        native_unit_of_measurement=UnitOfTime.HOURS,
        entity_category=EntityCategory.CONFIG,
        icon='mdi:timer-cog',
        native_min_value=0,
        native_max_value=12,
        native_step=1,
        entity_registry_enabled_default=False
    )
)

ERV_NUMBERS: tuple[PanasonicNumberDescription, ...] = (
    PanasonicNumberDescription(
        key=ERV_TARGET_TEMPERATURE,
        name="Target Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_category=EntityCategory.CONFIG,
        icon='mdi:thermometer',
        native_min_value=-128,
        native_max_value=127,
        native_step=1,
        entity_registry_enabled_default=False
    ),
    PanasonicNumberDescription(
        key=ERV_TIMER_ON,
        name="Timer On",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        entity_category=EntityCategory.CONFIG,
        icon='mdi:timer-cog',
        native_min_value=0,
        native_max_value=1440,
        native_step=1,
        entity_registry_enabled_default=False
    )
)

@dataclass
class PanasonicSelectDescription(
    SelectEntityDescription
):
    """Class to describe an Panasonic select."""
    options_value: list[str] | None = None


AIRPURIFIER_SELECTS: tuple[PanasonicSelectDescription, ...] = (
    PanasonicSelectDescription(
        key=AIRPURIFIER_LIGHT,
        name="Light",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:brightness-5',
        options=["Light", "Dark", "Off"],
        options_value=["0", "1", "2"]
    ),
    PanasonicSelectDescription(
        key=AIRPURIFIER_RESERVED,
        name="Reserved",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:help',
        options=[],
        options_value=[]
    )
)

CLIMATE_SELECTS: tuple[PanasonicSelectDescription, ...] = (
    PanasonicSelectDescription(
        key=CLIMATE_FUZZY_MODE,
        name="Fuzzy Mode",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:home-thermometer-outline',
        options=["Better", "Too cloud", "Too hot", "Off", "On"],
        options_value=["0", "1", "2", "3", "4"],
    ),
    PanasonicSelectDescription(
        key=CLIMATE_ACTIVITY,
        name="Motion Detect",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:motion-sensor',
        options=["Off", "To human", "Not to human", "Auto"],
        options_value=["0", "1", "2", "3"]
    ),
    PanasonicSelectDescription(
        key=CLIMATE_INDICATOR_LIGHT,
        name="Indicator Light",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:lightbulb',
        options=["Light", "Dark", "Off"],
        options_value=["0", "1", "2"]
    ),
    PanasonicSelectDescription(
        key=CLIMATE_SWING_VERTICAL_LEVEL,
        name="Vertical Fan Level",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:fan',
        options=["Auto", "1", "2", "3", "4"],
        options_value=["0", "1", "2", "3", "4"],
    ),
    PanasonicSelectDescription(
        key=CLIMATE_SWING_HORIZONTAL_LEVEL,
        name="Horizontal Fan Level",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:fan',
        options=["Auto", "1", "2", "3", "4"],
        options_value=["0", "1", "2", "3", "4"],
    ),
)

DEHUMIDIFIER_SELECTS: tuple[PanasonicSelectDescription, ...] = (
    PanasonicSelectDescription(
        key=DEHUMIDIFIER_FAN_SPEED,
        name="Fan Speed",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:fan',
        options=["Auto", "Slience", "Standard", "Speed"],
        options_value=["0", "1", "2", "3"],
    ),
    PanasonicSelectDescription(
        key=DEHUMIDIFIER_FAN_MODE,
        name="Fan Mode",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:fan-speed-1',
        options=["Fixed", "Down", "Up", "Both", "Side"],
        options_value=["0", "1", "2", "3", "4"]
    )
)

ERV_SELECTS: tuple[PanasonicSelectDescription, ...] = (
    PanasonicSelectDescription(
        key=ERV_VENTILATE_MODE,
        name="Ventilate Mode",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:home-thermometer',
        options=["Auto", "Ventilate", "Normal"],
        options_value=["0", "1", "2"],
    ),
    PanasonicSelectDescription(
        key=ERV_PRE_HEAT_COOL,
        name="Pre Head/Cool",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:home-thermometer-outline',
        options=["Disabled", "30min", "60min"],
        options_value=["0", "1", "2"]
    )
)

FRIDGE_SELECTS: tuple[PanasonicSelectDescription, ...] = (
    PanasonicSelectDescription(
        key=FRIDGE_FREEZER_MODE,
        name="Freezer mode",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:fridge-top',
        options=["Weak", "Medium", "Strong"],
        options_value=["0", "2", "4"],
    ),
    PanasonicSelectDescription(
        key=FRIDGE_CHAMBER_MODE,
        name="Chamber Mode",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:fridge-bottom',
        options=["Weak", "Medium", "Strong"],
        options_value=["0", "2", "4"],
    ),
    PanasonicSelectDescription(
        key=FRIDGE_THAW_MODE,
        name="Thaw Mode",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:fridge-outline',
        options=["Weak", "Medium", "Strong"],
        options_value=["0", "2", "4"],
    )
)

WASHING_MACHINE_SELECTS: tuple[PanasonicSelectDescription, ...] = (
    PanasonicSelectDescription(
        key=WASHING_MACHINE_PROGRESS,
        name="Progress",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:washing-machine',
        options=["Standard", "Soft Wash", "Strong Wash", "Wash with Shirt", "Wash with Blanket", "Wash with High-end clothing", "Wash with Woolen fabrics", "User-defined Wash", "Soak Wash", "Dry Clean", "Quick Wash", "Tank Wash", "Wash with Warm Water"],
        options_value=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    ),
    PanasonicSelectDescription(
        key=WASHING_MACHINE_TIMER,
        name="Appointment Time",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:clock',
        options=["0", "1", "2", "3"],
        options_value=["0", "1", "2", "3"]
    ),
    PanasonicSelectDescription(
        key=WASHING_MACHINE_POSTPONE_DRYING,
        name="Postpone Drying",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:clock',
        options=["Off", "1", "2", "3", "4", "5", "6", "7", "8"],
        options_value=["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    )
)


@dataclass
class PanasonicSensorDescription(
    SensorEntityDescription
):
    """Class to describe an Panasonic sensor."""


AIRPURIFIER_SENSORS: tuple[PanasonicSensorDescription, ...] = (
    PanasonicSensorDescription(
        key=AIRPURIFIER_AIR_QUALITY,
        name="Air Quality",
        device_class= SensorDeviceClass.AQI,
        icon='mdi:leaf'
    ),
    PanasonicSensorDescription(
        key=AIRPURIFIER_PM25,
        name="PM2.5",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM25,
        icon="mdi:chemical-weapon"
    ),
    PanasonicSensorDescription(
        key=AIRPURIFIER_RUNNING_TIME,
        name="Running Time",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:clock-outline"
    )
)

CLIMATE_SENSORS: tuple[PanasonicSensorDescription, ...] = (
    PanasonicSensorDescription(
        key=CLIMATE_TEMPERATURE_INDOOR,
        name="Inside Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer"
    ),
    PanasonicSensorDescription(
        key=CLIMATE_ERROR_CODE,
        name="Error Code",
        icon="mdi:alert-circle"
    ),
    PanasonicSensorDescription(
        key=CLIMATE_TEMPERATURE_OUTDOOR,
        name="Outside Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer"
    ),
    PanasonicSensorDescription(
        key=CLIMATE_PM25,
        name="PM2.5",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM25,
        icon="mdi:chemical-weapon"
    ),
    PanasonicSensorDescription(
        key=CLIMATE_ENERGY,
        name="Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        icon="mdi:flash"
    )
)

DEHUMIDIFIER_SENSORS: tuple[PanasonicSensorDescription, ...] = (
    PanasonicSensorDescription(
        key=DEHUMIDIFIER_HUMIDITY_INDOOR,
        name="Indoor Humidity",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.HUMIDITY,
        icon="mdi:water-percent"
    ),
    PanasonicSensorDescription(
        key=DEHUMIDIFIER_PM10,
        name="PM10",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM10,
        icon="mdi:chemical-weapon"
    ),
    PanasonicSensorDescription(
        key=DEHUMIDIFIER_PM25,
        name="PM2.5",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM25,
        icon="mdi:chemical-weapon"
    ),
    PanasonicSensorDescription(
        key=DEHUMIDIFIER_ENERGY,
        name="Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        icon="mdi:flash"
    ),
    PanasonicSensorDescription(
        key=DEHUMIDIFIER_ERROR_CODE,
        name="Error Code",
        icon="mdi:alert-circle"
    )
)

ERV_SENSORS: tuple[PanasonicSensorDescription, ...] = (
    PanasonicSensorDescription(
        key=ERV_TEMPERATURE_IN,
        name="Temperature In",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer"
    ),
    PanasonicSensorDescription(
        key=ERV_TEMPERATURE_OUT,
        name="Temperature Outdoor",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer"
    ),
    PanasonicSensorDescription(
        key=ERV_ENERGY,
        name="Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        icon="mdi:flash"
    ),
    PanasonicSensorDescription(
        key=ERV_ERROR_CODE,
        name="Error Code",
        icon="mdi:alert-circle"
    )
)

FRIDGE_SENSORS: tuple[PanasonicSensorDescription, ...] = (
    PanasonicSensorDescription(
        key=FRIDGE_FREEZER_TEMPERATURE,
        name="Freezer Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon='mdi:fridge-top'
    ),
    PanasonicSensorDescription(
        key=FRIDGE_CHAMBER_TEMPERATURE,
        name="Chamber Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:fridge-bottom"
    ),
    PanasonicSensorDescription(
        key=FRIDGE_ENERGY,
        name="Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        icon="mdi:flash"
    ),
    PanasonicSensorDescription(
        key=FRIDGE_THAW_TEMPERATURE,
        name="Thaw Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:fridge-outline"
    ),
    PanasonicSensorDescription(
        key=FRIDGE_ERROR_CODE,
        name="Error Code",
        icon="mdi:alert-circle"
    ),
    PanasonicSensorDescription(
        key=FRIDGE_ERROR_CODE_JP,
        name="Error Code",
        icon="mdi:alert-circle"
    ),
    PanasonicSensorDescription(
        key=ENTITY_DOOR_OPENS,
        name="Monthly Door Open Times",
        icon="mdi:information-slab-symbol"
    ),
    PanasonicSensorDescription(
        key=ENTITY_MONTHLY_ENERGY,
        name="Monthly Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        icon="mdi:flash"
    )
)

WASHING_MACHINE_SENSORS: tuple[PanasonicSensorDescription, ...] = (
    PanasonicSensorDescription(
        key=WASHING_MACHINE_REMAING_WASH_TIME,
        name="Washing Remaining Time",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        icon="mdi:clock"
    ),
    PanasonicSensorDescription(
        key=WASHING_MACHINE_TIMER_REMAINING_TIME,
        name="Timer Remaining Time",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        icon="mdi:clock-outline"
    ),
    PanasonicSensorDescription(
        key=WASHING_MACHINE_ERROR_CODE,
        name="Error Code",
        icon="mdi:alert-circle"
    ),
    PanasonicSensorDescription(
        key=WASHING_MACHINE_CURRENT_MODE,
        name="Current Mode",
        device_class=SensorDeviceClass.ENUM,
        icon="mdi:washing-machine"
    ),
    PanasonicSensorDescription(
        key=WASHING_MACHINE_CURRENT_PROGRESS,
        name="Current Progress",
        device_class=SensorDeviceClass.ENUM,
        icon="mdi:progress-helper"
    ),
    PanasonicSensorDescription(
        key=WASHING_MACHINE_OPERATING_STATUS,
        name="Operating Status",
        device_class=SensorDeviceClass.ENUM,
        icon="mdi:washing-machine"
    ),
    PanasonicSensorDescription(
        key=ENTITY_WASH_TIMES,
        name="Monthly Washing Times",
        icon="mdi:information-slab-symbol"
    ),
    PanasonicSensorDescription(
        key=ENTITY_WATER_USED,
        name="Monthly Used Water",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        icon="mdi:water"
    ),
    PanasonicSensorDescription(
        key=WASHING_MACHINE_ENERGY,
        name="Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        icon="mdi:flash"
    ),
    PanasonicSensorDescription(
        key=WASHING_MACHINE_REMOTE_CONTROL,
        name="Remote Control",
        icon='mdi:cog'
    )
)

WEIGHT_PLATE_SENSORS: tuple[PanasonicSensorDescription, ...] = (
    PanasonicSensorDescription(
        key=WEIGHT_PLATE_FOOD_NAME,
        name="Food name",
        icon="mdi:food"
    ),
    PanasonicSensorDescription(
        key=WEIGHT_PLATE_BUY_DATE,
        name="Buy Date",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:clock"
    ),
    PanasonicSensorDescription(
        key=WEIGHT_PLATE_DUE_DATE,
        name="Due Date",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:clock-outline"
    ),
    PanasonicSensorDescription(
        key=WEIGHT_PLATE_MANAGEMENT_MODE,
        name="Management Mode",
        icon="mdi:cog"
    ),
    PanasonicSensorDescription(
        key=WEIGHT_PLATE_MANAGEMENT_VALUE,
        name="Management Value",
        icon="mdi:cog"
    ),
    PanasonicSensorDescription(
        key=WEIGHT_PLATE_AMOUNT_MAX,
        name="Max Amount",
        icon="mdi:cog"
    ),
    PanasonicSensorDescription(
        key=WEIGHT_PLATE_COMMUNICATION_MODE,
        name="Communication Mode",
        icon="mdi:cog"
    ),
    PanasonicSensorDescription(
        key=WEIGHT_PLATE_COMMUNICATION_TIME,
        name="Communication Time",
        icon="mdi:clock-outline"
    ),
    PanasonicSensorDescription(
        key=WEIGHT_PLATE_TOTAL_WEIGHT,
        name="Total Weight",
        device_class=SensorDeviceClass.WEIGHT,
        native_unit_of_measurement=UnitOfMass.GRAMS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:weight-gram"
    ),
    PanasonicSensorDescription(
        key=WEIGHT_PLATE_RESTORE_WEIGHT,
        name="Restore Weight",
        device_class=SensorDeviceClass.WEIGHT,
        native_unit_of_measurement=UnitOfMass.GRAMS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:weight-gram"
    ),
    PanasonicSensorDescription(
        key=WEIGHT_PLATE_LOW_BATTERY,
        name="Low Battery",
        icon="mdi:battery-alert"
    )
)

@dataclass
class PanasonicSwitchDescription(
    SwitchEntityDescription
):
    """Class to describe an Panasonic switch."""


AIRPURIFIER_SWITCHES: tuple[PanasonicSwitchDescription, ...] = (
    PanasonicSwitchDescription(
        key=AIRPURIFIER_RESET_FILTER_NOTIFY,
        name="Reset Filter Notify",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:volume-high'
    ),
    PanasonicSwitchDescription(
        key=AIRPURIFIER_BUZZER,
        name="Buzzer",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:volume-high'
    )
)

CLIMATE_SWITCHES: tuple[PanasonicSwitchDescription, ...] = (
    PanasonicSwitchDescription(
        key=CLIMATE_AIRFRESH_MODE,
        name=" nanoe™ X",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:atom-variant'
    ),
    PanasonicSwitchDescription(
        key=CLIMATE_ANTI_MILDEW,
        name="Anti Mildew",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:weather-dust'
    ),
    PanasonicSwitchDescription(
        key=CLIMATE_AUTO_CLEAN,
        name="Auto Clean",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:broom'
    ),
    PanasonicSwitchDescription(
        key=CLIMATE_BUZZER,
        name="Buzzer",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:volume-source'
    ),
    PanasonicSwitchDescription(
        key=CLIMATE_MONITOR_MILDEW,
        name="Mildew Monitor",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:mushroom'
    )
)

DEHUMIDIFIER_SWITCHES: tuple[PanasonicSwitchDescription, ...] = (
    PanasonicSwitchDescription(
        key=DEHUMIDIFIER_AIRFRESH_MODE,
        name=" nanoe™ X",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:atom-variant'
    ),
    PanasonicSwitchDescription(
        key=DEHUMIDIFIER_BUZZER,
        name="Buzzer",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:volume-high'
    )
)

FRIDGE_SWITCHES: tuple[PanasonicSwitchDescription, ...] = (
    PanasonicSwitchDescription(
        key=FRIDGE_DEFROST_SETTING,
        name=" nanoe™ X",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:snowflake-melt'
    ),
    PanasonicSwitchDescription(
        key=FRIDGE_ECO,
        name="ECO",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:sprout'
    ),
    PanasonicSwitchDescription(
        key=FRIDGE_NANOEX,
        name=" nanoe™ X",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:atom-variant'
    ),
    PanasonicSwitchDescription(
        key=FRIDGE_FAST_ICE_MAKING,
        name="Fast Ice Making",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:snowflake'
    ),
    PanasonicSwitchDescription(
        key=FRIDGE_FRESH_QUICK_FREZZE,
        name="Fresh Quick Freeze",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:snowflake-check'
    ),
    PanasonicSwitchDescription(
        key=FRIDGE_WINTER_MDOE,
        name="Winter Mode",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:snowman'
    ),
    PanasonicSwitchDescription(
        key=FRIDGE_SHOPPING_MODE,
        name="Shopping Mode",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:shopping'
    ),
    PanasonicSwitchDescription(
        key=FRIDGE_GO_OUT_MODE,
        name="Go Out Mode",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:logout'
    )
)

WASHING_MACHINE_SWITCHES: tuple[PanasonicSwitchDescription, ...] = (
    PanasonicSwitchDescription(
        key=WASHING_MACHINE_ENABLE,
        name="Pause/Start",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:play-pause'
    ),
    PanasonicSwitchDescription(
        key=WASHING_MACHINE_WARM_WATER,
        name="Warm Water",
        device_class=SwitchDeviceClass.SWITCH,
        icon='mdi:heat-wave'
    )
)

SAA_BINARY_SENSORS = {
    DEVICE_TYPE_AIRPURIFIER: AIRPURIFIER_BINARY_SENSORS,
    DEVICE_TYPE_CLIMATE: CLIMATE_BINARY_SENSORS,
    DEVICE_TYPE_DEHUMIDIFIER: DEHUMIDIFIER_BINARY_SENSORS,
    DEVICE_TYPE_ERV: ERV_BINARY_SENSORS,
    DEVICE_TYPE_FRIDGE: FRIDGE_BINARY_SENSORS,
    DEVICE_TYPE_WASHING_MACHINE: WASHING_MACHINE_BINARY_SENSORS
}

SAA_NUMBERS = {
    DEVICE_TYPE_CLIMATE: CLIMATE_NUMBERS,
    DEVICE_TYPE_DEHUMIDIFIER: DEHUMIDIFIER_NUMBERS,
    DEVICE_TYPE_ERV: ERV_NUMBERS
}

SAA_SELECTS = {
    DEVICE_TYPE_AIRPURIFIER: AIRPURIFIER_SELECTS,
    DEVICE_TYPE_CLIMATE: CLIMATE_SELECTS,
    DEVICE_TYPE_DEHUMIDIFIER: DEHUMIDIFIER_SELECTS,
    DEVICE_TYPE_ERV: ERV_SELECTS,
    DEVICE_TYPE_FRIDGE: FRIDGE_SELECTS
}

SAA_SENSORS = {
    DEVICE_TYPE_AIRPURIFIER: AIRPURIFIER_SENSORS,
    DEVICE_TYPE_CLIMATE: CLIMATE_SENSORS,
    DEVICE_TYPE_DEHUMIDIFIER: DEHUMIDIFIER_SENSORS,
    DEVICE_TYPE_ERV: ERV_SENSORS,
    DEVICE_TYPE_FRIDGE: FRIDGE_SENSORS
}

SAA_SWITCHES = {
    DEVICE_TYPE_AIRPURIFIER: AIRPURIFIER_SWITCHES,
    DEVICE_TYPE_CLIMATE: CLIMATE_SWITCHES,
    DEVICE_TYPE_DEHUMIDIFIER: DEHUMIDIFIER_SWITCHES,
    DEVICE_TYPE_FRIDGE: FRIDGE_SWITCHES
}
