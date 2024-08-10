""" Panasonic Smart Home Climate"""
import logging
import asyncio

from homeassistant.components.climate import ClimateEntityFeature, ClimateEntity
from homeassistant.const import (
    UnitOfTemperature,
    ATTR_TEMPERATURE,
    STATE_UNAVAILABLE
)
from homeassistant.components.climate.const import (
    HVACMode,
    PRESET_NONE,
    SWING_ON,
    SWING_OFF,
    SWING_BOTH,
    SWING_VERTICAL,
    SWING_HORIZONTAL
)

from .core.base import PanasonicBaseEntity
from .core.const import (
    DOMAIN,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DEVICE_TYPE_CLIMATE,
    DEVICE_TYPE_ERV,
    CLIMATE_AVAILABLE_FAN_MODES,
    CLIMATE_AVAILABLE_MODES,
    CLIMATE_AVAILABLE_PRESET_MODES,
    CLIMATE_FAN_SPEED,
    CLIMATE_OPERATING_MODE,
    CLIMATE_POWER,
    CLIMATE_MAXIMUM_TEMPERATURE,
    CLIMATE_MINIMUM_TEMPERATURE,
    CLIMATE_SWING_VERTICAL_LEVEL,
    CLIMATE_SWING_HORIZONTAL_LEVEL,
    CLIMATE_TARGET_TEMPERATURE,
    CLIMATE_TEMPERATURE_INDOOR,
    CLIMATE_TEMPERATURE_STEP,
    CLIMATE_PRESET_MODE,
    CLIMATE_SWING_MODE,
    ERV_POWER,
    ERV_FAN_SPEED,
    ERV_OPERATING_MODE,
    ERV_AVAILABLE_MODES,
    ERV_AVAILABLE_FAN_MODES,
    ERV_TARGET_TEMPERATURE,
    ERV_TEMPERATURE_IN,
    ERV_MINIMUM_TEMPERATURE,
    ERV_MAXIMUM_TEMPERATURE
)

_LOGGER = logging.getLogger(__name__)

PANASONIC_CLIMATE_TYPE = [
    str(DEVICE_TYPE_CLIMATE),
    str(DEVICE_TYPE_ERV)
]

def get_key_from_dict(dictionary, value):
    """ get key from dictionary by value"""
    for key, val in dictionary.items():
        if value == val:
            return key
    return None

async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data
    climate = []

    for device_gwid, info in devices.items():
        device_type = info.get("DeviceType", None)
        if (device_type and
                str(device_type) in PANASONIC_CLIMATE_TYPE):
            if not client.is_supported(info.get("ModelType", "")):
                continue
            for dev in info["Devices"]:
                device_id = dev["DeviceID"]
                climate.append(
                    PanasonicClimate(
                        coordinator,
                        device_gwid,
                        device_id,
                        client,
                        info,
                    )
                )

    async_add_entities(climate, True)

    return True


class PanasonicClimate(PanasonicBaseEntity, ClimateEntity):
    _swing_mode = SWING_OFF

    def __init__(
        self,
        coordinator,
        device_gwid,
        device_id,
        client,
        info,
    ):
        super().__init__(coordinator, device_gwid, device_id, client, info)
        device_type = info.get("DeviceType", None)
        self._device_type = int(device_type)

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        features = ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TURN_OFF | ClimateEntityFeature.TURN_ON
        status = self.get_status(self.coordinator.data)

        preset_mode = False
        if self._device_type == DEVICE_TYPE_CLIMATE:
            if (status.get(CLIMATE_SWING_VERTICAL_LEVEL, None) is not None and
                (status.get(CLIMATE_SWING_HORIZONTAL_LEVEL, None) is not None)):
                features |= ClimateEntityFeature.SWING_MODE

            if status.get(CLIMATE_FAN_SPEED, None) is not None:
                features |= ClimateEntityFeature.FAN_MODE

            for st in status:
                if st in CLIMATE_AVAILABLE_PRESET_MODES:
                    preset_mode = True
                    break

        elif self._device_type == DEVICE_TYPE_ERV:
            if status.get(ERV_FAN_SPEED, None) is not None:
                features |= ClimateEntityFeature.FAN_MODE

        if preset_mode:
            features |= ClimateEntityFeature.PRESET_MODE

        return features

    @property
    def temperature_unit(self) -> str:
        return UnitOfTemperature.CELSIUS

    @property
    def hvac_mode(self) -> str:
        """Return hvac operation ie. heat, cool mode."""
        status = self.get_status(self.coordinator.data)
        if self._device_type == DEVICE_TYPE_ERV:
            power = ERV_POWER
            operation_mode = ERV_OPERATING_MODE
            available_modes = ERV_AVAILABLE_MODES
        else:
            power = CLIMATE_POWER
            operation_mode = CLIMATE_OPERATING_MODE
            available_modes = CLIMATE_AVAILABLE_MODES

        is_on = bool(int(status.get(power, 0)))

        if is_on:
            if status.get(operation_mode, None) is None:
                _LOGGER.error("Can not get status!")
                return HVACMode.OFF
            value = status.get(operation_mode, None)
            #if value is None:
            #    return STATE_UNAVAILABLE
            return get_key_from_dict(available_modes, int(value))

        return HVACMode.OFF

    @property
    def hvac_modes(self) -> list:
        """Return the list of available hvac operation modes."""
        hvac_modes = [HVACMode.OFF]
        available_modes = {}

        if self._device_type == DEVICE_TYPE_ERV:
            rng = self.client.get_range(self.device_gwid, ERV_OPERATING_MODE)
            available_modes = ERV_AVAILABLE_MODES
        else:
            rng = self.client.get_range(self.device_gwid, CLIMATE_OPERATING_MODE)
            available_modes = CLIMATE_AVAILABLE_MODES

        for mode, value in available_modes.items():
            if value >= 0:
                for _, value2 in rng.items():
                    if value == value2:
                        hvac_modes.append(mode)
                        break
        return hvac_modes

    async def async_set_hvac_mode(self, hvac_mode) -> None:
        """Set new target hvac mode."""
        status = self.get_status(self.coordinator.data)
        if self._device_type == DEVICE_TYPE_ERV:
            power = ERV_POWER
            operation_mode = ERV_OPERATING_MODE
        else:
            power = CLIMATE_POWER
            operation_mode = CLIMATE_OPERATING_MODE

        is_on = bool(int(status.get(power, 0)))
        gwid = self.device_gwid
        device_id = self.device_id
        if hvac_mode == HVACMode.OFF:
            await self.client.set_device(gwid, device_id, power, 0)
        else:
            mode = CLIMATE_AVAILABLE_MODES.get(hvac_mode)
            await self.client.set_device(gwid, device_id, operation_mode, mode)
            if not is_on:
                await self.client.set_device(gwid, device_id, power, 1)

        await asyncio.sleep(1)
        await self.client.update_device(gwid, device_id)
        self.async_write_ha_state()

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode, e.g., home, away, temp."""
        status = self.get_status(self.coordinator.data)

        is_on = status.get(CLIMATE_POWER, None)
        #if is_on is None:
        #    return STATE_UNAVAILABLE
        preset_mode = PRESET_NONE
        for key, mode in CLIMATE_AVAILABLE_PRESET_MODES.items():
            if key in status and status[key]:
                preset_mode = mode
                break

        preset_mode = preset_mode if bool(int(is_on)) else PRESET_NONE

        return preset_mode

    @property
    def preset_modes(self) -> list:
        """Return a list of available preset modes."""
        status = self.get_status(self.coordinator.data)
        modes = [PRESET_NONE]

        for mode in status:
            if mode in CLIMATE_AVAILABLE_PRESET_MODES:
                modes.append(CLIMATE_AVAILABLE_PRESET_MODES[mode])

        return modes

    async def async_set_preset_mode(self, preset_mode) -> None:
        """Set new preset mode."""
        status = self.get_status(self.coordinator.data)
        is_on = bool(status.get(CLIMATE_POWER, 0))

        func = get_key_from_dict(CLIMATE_AVAILABLE_PRESET_MODES, preset_mode)
        gwid = self.device_gwid
        device_id = self.device_id

        await self.client.set_device(gwid, device_id, func, 1)
        if not is_on:
            await self.client.set_device(gwid, device_id, CLIMATE_POWER, 1)

        await self.client.update_device(gwid, device_id)
        self.async_write_ha_state()

    @property
    def fan_mode(self) -> str:
        """Return the fan setting."""
        status = self.get_status(self.coordinator.data)
        if self._device_type == DEVICE_TYPE_ERV:
            fan_mode = ERV_OPERATING_MODE
            available_fan_modes = ERV_AVAILABLE_FAN_MODES
        else:
            fan_mode = CLIMATE_FAN_SPEED
            available_fan_modes = CLIMATE_AVAILABLE_FAN_MODES

        mode = status.get(fan_mode, None)
        #if fan_mode is None:
        #    return STATE_UNAVAILABLE
        value = get_key_from_dict(available_fan_modes, int(mode))

        return value

    @property
    def fan_modes(self) -> list:
        """Return the list of available fan modes."""
        modes = []
        if self._device_type == DEVICE_TYPE_ERV:
            fan_mode = ERV_OPERATING_MODE
            available_fan_modes = ERV_AVAILABLE_FAN_MODES
        else:
            fan_mode = CLIMATE_FAN_SPEED
            available_fan_modes = CLIMATE_AVAILABLE_FAN_MODES

        rng = self.client.get_range(self.device_gwid, fan_mode)
        if "Max" in rng:
            max = rng.get("Max", 1)

            for mode, value in available_fan_modes.items():
                if max >= value:
                    modes.append(mode)

            if len(modes) <= 1:
                modes.append("Auto")
        else:
            modes = list(rng.keys())
        return modes

    async def async_set_fan_mode(self, mode) -> None:
        """Set new fan mode."""
        if self._device_type == DEVICE_TYPE_ERV:
            fan_mode = ERV_OPERATING_MODE
            available_fan_modes = ERV_AVAILABLE_FAN_MODES
        else:
            fan_mode = CLIMATE_FAN_SPEED
            available_fan_modes = CLIMATE_AVAILABLE_FAN_MODES

        value = available_fan_modes[mode]
        gwid = self.device_gwid
        device_id = self.device_id

        await self.client.set_device(gwid, device_id, fan_mode, value)
        await self.client.update_device(gwid, device_id)
        self.async_write_ha_state()

    @property
    def swing_mode(self) -> str:
        """Return the swing setting."""
        status = self.get_status(self.coordinator.data)

        swing_vertical = status.get(CLIMATE_SWING_VERTICAL_LEVEL, None)
        swing_horizontal = status.get(CLIMATE_SWING_HORIZONTAL_LEVEL, None)
        #if swing_horizontal is None or swing_vertical is None:
        #    return STATE_UNAVAILABLE
        swing_vertical = bool(swing_vertical)
        swing_horizontal = bool(swing_horizontal)
        mode = SWING_OFF
        if swing_vertical or swing_horizontal:
            mode = SWING_ON

        if swing_vertical and swing_horizontal:
            mode = SWING_BOTH

        elif swing_vertical:
            mode = SWING_VERTICAL

        elif swing_horizontal:
            mode = SWING_HORIZONTAL

        self._swing_mode = mode
        return mode

    @property
    def swing_modes(self) -> list:
        """Return the list of available swing modes.

        Requires ClimateEntityFeature.SWING_MODE.
        """
        status = self.get_status(self.coordinator.data)
        swing_modes = [SWING_ON, SWING_OFF]

        swing_vertical = status.get(CLIMATE_SWING_VERTICAL_LEVEL, None)
        if swing_vertical is not None:
            swing_modes.append(SWING_VERTICAL)

        swing_horizontal = status.get(CLIMATE_SWING_HORIZONTAL_LEVEL, None)
        if swing_horizontal is not None:
            swing_modes.append(SWING_HORIZONTAL)

        if swing_vertical is not None and swing_horizontal  is not None:
            swing_modes.append(SWING_BOTH)

        return swing_modes

    async def async_set_swing_mode(self, swing_mode) -> None:
        """Set new target swing operation."""
        gwid = self.device_gwid
        device_id = self.device_id

        if swing_mode == SWING_ON:
            if self._swing_mode == SWING_HORIZONTAL:
                mode = 1
            if self._swing_mode == SWING_VERTICAL:
                mode = 2

        elif swing_mode == SWING_OFF:
            mode = 0

        elif swing_mode == SWING_HORIZONTAL:
            mode = 1
        elif swing_mode == SWING_VERTICAL:
            mode = 2

        elif swing_mode == SWING_BOTH:
            mode = 4

        await self.client.set_device(gwid, device_id, CLIMATE_SWING_MODE, mode)
        await self.client.update_device(gwid, device_id)
        self.async_write_ha_state()

    @property
    def target_temperature(self) -> int:
        """Return the temperature we try to reach."""
        status = self.get_status(self.coordinator.data)
        if self._device_type == DEVICE_TYPE_ERV:
            return float(status.get(ERV_TARGET_TEMPERATURE, 0))
        else:
            return float(status.get(CLIMATE_TARGET_TEMPERATURE, 0))

    async def async_set_temperature(self, **kwargs):
        """ Set new target temperature """
        temp = kwargs.get(ATTR_TEMPERATURE)
        gwid = self.device_gwid
        device_id = self.device_id
        if self._device_type == DEVICE_TYPE_ERV:
            await self.client.set_device(gwid, device_id, ERV_TARGET_TEMPERATURE, int(temp))
        else:
            await self.client.set_device(gwid, device_id, CLIMATE_TARGET_TEMPERATURE, int(temp))
        await self.client.update_device(gwid, device_id)
        self.async_write_ha_state()

    @property
    def current_temperature(self) -> int:
        """Return the current temperature."""
        status = self.get_status(self.coordinator.data)
        if self._device_type == DEVICE_TYPE_ERV:
            return float(status.get(ERV_TEMPERATURE_IN, 0))
        else:
            return float(status.get(CLIMATE_TEMPERATURE_INDOOR, 0))

    @property
    def min_temp(self) -> int:
        """ Return the minimum temperature """
        if self._device_type == DEVICE_TYPE_ERV:
            rng = self.client.get_range(self.device_gwid, ERV_TARGET_TEMPERATURE)
            return rng.get("Min", ERV_MINIMUM_TEMPERATURE)

        rng = self.client.get_range(self.device_gwid, CLIMATE_TARGET_TEMPERATURE)
        return rng.get("Min", CLIMATE_MINIMUM_TEMPERATURE)

    @property
    def max_temp(self) -> int:
        """ Return the maximum temperature """
        if self._device_type == DEVICE_TYPE_ERV:
            rng = self.client.get_range(self.device_gwid, ERV_TARGET_TEMPERATURE)
            return rng.get("Max", ERV_MAXIMUM_TEMPERATURE)

        rng = self.client.get_range(self.device_gwid, CLIMATE_TARGET_TEMPERATURE)
        return rng.get("Max", CLIMATE_MAXIMUM_TEMPERATURE)

    @property
    def target_temperature_step(self) -> float:
        """ Return temperature step """
        return CLIMATE_TEMPERATURE_STEP