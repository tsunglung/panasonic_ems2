"""Constants of the Panasonic Smart Home component."""

from dataclasses import dataclass

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
    HVAC_MODE_OFF,
    HVAC_MODE_COOL,
    HVAC_MODE_DRY,
    HVAC_MODE_HEAT,
    HVAC_MODE_AUTO,
    HVAC_MODE_FAN_ONLY,
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
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume
)

DOMAIN = "panasonic_ems2"

DOMAINS = [
#    "binary_sensor",
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

DEVICE_TYPE_CLIMATE = 1
DEVICE_TYPE_FRIDGE = 2
DEVICE_TYPE_WASHING_MACHINE = 3
DEVICE_TYPE_DEHUMIDIFIER = 4
DEVICE_TYPE_AIRPURIFIER = 8
DEVICE_TYPE_FAN = 15

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
AIRPURIFIER_MONTHLY_ENERGY = "0xA0"  # alternative

AIRPURIFIER_NANOEX_PRESET = "nanoe™ X"
AIRPURIFIER_PRESET_MODES = {
    AIRPURIFIER_NANOEX: AIRPURIFIER_NANOEX_PRESET,
}

CLIMATE_AVAILABLE_MODES = {
    HVAC_MODE_OFF: -1,
    HVAC_MODE_COOL: 0,
    HVAC_MODE_DRY: 1,
    HVAC_MODE_FAN_ONLY: 2,
    HVAC_MODE_AUTO: 3,
    HVAC_MODE_HEAT: 4
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
CLIMATE_MONTHLY_ENERGY = "0xA0"  # alternative

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
                CLIMATE_MONITOR_MILDEW,
                CLIMATE_PM25,
                CLIMATE_61
            ]

DEHUMIDIFIER_POWER = "0x00"
DEHUMIDIFIER_MODE = "0x01"
DEHUMIDIFIER_TIMER_OFF = "0x02"
DEHUMIDIFIER_RELATIVE_HUMIDITY = "0x03"
DEHUMIDIFIER_TARGET_HUMIDITY = "0x04"
DEHUMIDIFIER_HUMIDITY_INDOOR = "0x07"
DEHUMIDIFIER_FAN_SPEED = "0x09"
DEHUMIDIFIER_WATER_TANK_STATUS = "0x0A"
DEHUMIDIFIER_AIRFRESH_MODE = "0x0D"
DEHUMIDIFIER_FAN_MODE = "0x0E"
DEHUMIDIFIER_BUZZER = "0x18"
DEHUMIDIFIER_ENERGY = "0x1D"
DEHUMIDIFIER_50 = "0x50"
DEHUMIDIFIER_PM25 = "0x53"
DEHUMIDIFIER_TIMER_ON = "0x55"
DEHUMIDIFIER_MONTHLY_ENERGY = "0xA0"  # alternative

DEHUMIDIFIER_MAX_HUMIDITY = 70
DEHUMIDIFIER_MIN_HUMIDITY = 40

DEHUMIDIFIER_DEFAULT_MODES = {
    "Auto": 0,
    "Set": 1,
    "Continuous": 2,
    "Cloth Dry": 3
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
FRIDGE_63 = "0x63"
FRIDGE_MONTHLY_ENERGY = "0xA0"  # alternative
FRIDGE_DOOR_OPENS = "0xA1"  # alternative

FRIDGE_XGS_COMMANDS = [
                FRIDGE_ECO,
                FRIDGE_FREEZER_TEMPERATURE,
                FRIDGE_CHAMBER_TEMPERATURE,
                FRIDGE_THAW_TEMPERATURE,
                FRIDGE_ENERGY,
                FRIDGE_NANOEX
            ]

WASHING_MACHINE_MODELS = ["HDH"]

WASHING_MACHINE_POWER = "0x00"
WASHING_MACHINE_ENABLE = "0x01"
WASHING_MACHINE_REMAING_WASH_TIME= "0x13"
WASHING_MACHINE_TIMER = "0x14"
WASHING_MACHINE_TIMER_REMAINING_TIME = "0x15"
WASHING_MACHINE_ERROR_CODE = "0x19"
WASHING_MACHINE_ENERGY = "0x1E"
WASHING_MACHINE_OPERATING_STATUS = "0x50"
WASHING_MACHINE_CURRENT_MODE = "0x54"
WASHING_MACHINE_CURRENT_PROGRESS = "0x55"
WASHING_MACHINE_DELAY_DRYING = "0x61"
WASHING_MACHINE_PROGRESS = "0x64"
WASHING_MACHINE_WARM_WATER = "0x69"
WASHING_MACHINE_MONTHLY_ENERGY = "0xA0"  # alternative
WASHING_MACHINE_WASH_TIMES = "0xA1"  # alternative
WASHING_MACHINE_WATER_USED = "0xA2"   # alternative

COMMANDS_TYPE= {
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
        DEHUMIDIFIER_PM25,
        DEHUMIDIFIER_TIMER_ON
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
#        WASHING_MACHINE_POWER,
        WASHING_MACHINE_ENABLE,
        WASHING_MACHINE_REMAING_WASH_TIME,
        WASHING_MACHINE_TIMER,
        WASHING_MACHINE_TIMER_REMAINING_TIME,
        WASHING_MACHINE_ENERGY,
        WASHING_MACHINE_OPERATING_STATUS,
        WASHING_MACHINE_CURRENT_MODE,
        WASHING_MACHINE_CURRENT_PROGRESS,
        WASHING_MACHINE_DELAY_DRYING,
        WASHING_MACHINE_PROGRESS,
        WASHING_MACHINE_WARM_WATER
    ],
    str(DEVICE_TYPE_AIRPURIFIER): [
        AIRPURIFIER_OPERATING_MODE,
        AIRPURIFIER_TIMER_ON,
        AIRPURIFIER_TIMER_OFF,
        AIRPURIFIER_AIR_QUALITY,
        AIRPURIFIER_NANOEX,
        AIRPURIFIER_BUZZER,
        AIRPURIFIER_PM25,
        AIRPURIFIER_LIGHT
    ]
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
        WASHING_MACHINE_PROGRESS: 100,
        WASHING_MACHINE_WARM_WATER: 105
    }
}


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
        icon='mdi:broom',
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
        icon='mdi:broom',
        options=["Light", "Dark", "Off"],
        options_value=["0", "1", "2"]
    ),
    PanasonicSelectDescription(
        key=CLIMATE_SWING_VERTICAL_LEVEL,
        name="Vertical Fan Level",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:broom',
        options=["Auto", "1", "2", "3", "4"],
        options_value=["0", "1", "2", "3", "4"],
    ),
    PanasonicSelectDescription(
        key=CLIMATE_SWING_HORIZONTAL_LEVEL,
        name="Horizontal Fan Level",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:broom',
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
        icon='mdi:broom',
        options=["Standard", "Custom", "Immerse", "Quick"],
        options_value=["0", "1", "2", "3"],
    ),
    PanasonicSelectDescription(
        key=WASHING_MACHINE_TIMER,
        name="Appointment Time",
        entity_category=EntityCategory.CONFIG,
        icon='mdi:clock',
        options=["0", "1", "2", "3"],
        options_value=["0", "1", "2", "3"]
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
        key=DEHUMIDIFIER_WATER_TANK_STATUS,
        name="Water Tank",
        icon="mdi:cup-water"
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
        key=FRIDGE_DOOR_OPENS,
        name="Monthly Door Open Times",
        icon="mdi:information-slab-symbol"
    ),
    PanasonicSensorDescription(
        key=FRIDGE_MONTHLY_ENERGY,
        name="Monthly Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        icon="mdi:flash"
    ),
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
        key=WASHING_MACHINE_WASH_TIMES,
        name="Monthly Washing Times",
        icon="mdi:information-slab-symbol"
    ),
    PanasonicSensorDescription(
        key=WASHING_MACHINE_WATER_USED,
        name="Monthly Used Water",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        icon="mdi:water"
    ),
    PanasonicSensorDescription(
        key=WASHING_MACHINE_MONTHLY_ENERGY,
        name="Monthly Energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        icon="mdi:flash"
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

SAA_NUMBERS = {
    DEVICE_TYPE_CLIMATE: CLIMATE_NUMBERS,
    DEVICE_TYPE_DEHUMIDIFIER: DEHUMIDIFIER_NUMBERS,
}

SAA_SELECTS = {
    DEVICE_TYPE_AIRPURIFIER: AIRPURIFIER_SELECTS,
    DEVICE_TYPE_CLIMATE: CLIMATE_SELECTS,
    DEVICE_TYPE_DEHUMIDIFIER: DEHUMIDIFIER_SELECTS,
    DEVICE_TYPE_FRIDGE: FRIDGE_SELECTS
}

SAA_SENSORS = {
    DEVICE_TYPE_AIRPURIFIER: AIRPURIFIER_SENSORS,
    DEVICE_TYPE_CLIMATE: CLIMATE_SENSORS,
    DEVICE_TYPE_DEHUMIDIFIER: DEHUMIDIFIER_SENSORS,
    DEVICE_TYPE_FRIDGE: FRIDGE_SENSORS
}

SAA_SWITCHES = {
    DEVICE_TYPE_AIRPURIFIER: AIRPURIFIER_SWITCHES,
    DEVICE_TYPE_CLIMATE: CLIMATE_SWITCHES,
    DEVICE_TYPE_DEHUMIDIFIER: DEHUMIDIFIER_SWITCHES,
    DEVICE_TYPE_FRIDGE: FRIDGE_SWITCHES
}
