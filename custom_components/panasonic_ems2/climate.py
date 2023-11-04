""" Panasonic Smart Home Climate"""
import logging
import asyncio

from homeassistant.components.climate import ClimateEntity
from homeassistant.const import (
    TEMP_CELSIUS,
    ATTR_TEMPERATURE,
    STATE_UNAVAILABLE
)
from homeassistant.components.climate.const import (
    HVAC_MODE_OFF,
    PRESET_NONE,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_FAN_MODE,
    SUPPORT_SWING_MODE,
    SUPPORT_PRESET_MODE,
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
    CLIMATE_SWING_MODE
)

_LOGGER = logging.getLogger(__name__)

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
                int(device_type) == DEVICE_TYPE_CLIMATE):
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

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        features = SUPPORT_TARGET_TEMPERATURE
        status = self.get_status(self.coordinator.data)

        if (status.get(CLIMATE_SWING_VERTICAL_LEVEL, None) is not None and
            (status.get(CLIMATE_SWING_HORIZONTAL_LEVEL, None) is not None)):
            features |= SUPPORT_SWING_MODE

        if status.get(CLIMATE_FAN_SPEED, None) is not None:
            features |= SUPPORT_FAN_MODE

        preset_mode = False
        for st in status:
            if st in CLIMATE_AVAILABLE_PRESET_MODES:
                preset_mode = True
                break
        if preset_mode:
            features |= SUPPORT_PRESET_MODE

        return features

    @property
    def temperature_unit(self) -> str:
        return TEMP_CELSIUS

    @property
    def hvac_mode(self) -> str:
        """Return hvac operation ie. heat, cool mode."""
        status = self.get_status(self.coordinator.data)
        is_on = bool(int(status.get(CLIMATE_POWER, 0)))

        if is_on:
            if status.get(CLIMATE_OPERATING_MODE, None) is None:
                _LOGGER.error("Can not get status!")
                return HVAC_MODE_OFF
            value = status.get(CLIMATE_OPERATING_MODE, None)
            #if value is None:
            #    return STATE_UNAVAILABLE
            return get_key_from_dict(CLIMATE_AVAILABLE_MODES, int(value))

        return HVAC_MODE_OFF

    @property
    def hvac_modes(self) -> list:
        """Return the list of available hvac operation modes."""
        hvac_modes = [HVAC_MODE_OFF]
        rng = self.client.get_range(self.device_gwid, CLIMATE_OPERATING_MODE)

        for mode, value in CLIMATE_AVAILABLE_MODES.items():
            if value >= 0:
                for _, value2 in rng.items():
                    if value == value2:
                        hvac_modes.append(mode)
                        break

        return hvac_modes

    async def async_set_hvac_mode(self, hvac_mode) -> None:
        """Set new target hvac mode."""
        status = self.get_status(self.coordinator.data)

        is_on = bool(int(status.get(CLIMATE_POWER, 0)))
        gwid = self.device_gwid
        device_id = self.device_id
        if hvac_mode == HVAC_MODE_OFF:
            await self.client.set_device(gwid, device_id, CLIMATE_POWER, 0)
        else:
            mode = CLIMATE_AVAILABLE_MODES.get(hvac_mode)
            await self.client.set_device(gwid, device_id, CLIMATE_OPERATING_MODE, mode)
            if not is_on:
                await self.client.set_device(gwid, device_id, CLIMATE_POWER, 1)

        await asyncio.sleep(1)
        await self.coordinator.async_request_refresh()

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

        await self.coordinator.async_request_refresh()

    @property
    def fan_mode(self) -> str:
        """Return the fan setting."""
        status = self.get_status(self.coordinator.data)
        fan_mode = status.get(CLIMATE_FAN_SPEED, None)
        #if fan_mode is None:
        #    return STATE_UNAVAILABLE
        value = get_key_from_dict(CLIMATE_AVAILABLE_FAN_MODES, int(fan_mode))

        return value

    @property
    def fan_modes(self) -> list:
        """Return the list of available fan modes."""
        modes = []
        rng = self.client.get_range(self.device_gwid, CLIMATE_FAN_SPEED)
        max = rng.get("Max", 1)

        for mode, value in CLIMATE_AVAILABLE_FAN_MODES.items():
            if max >= value:
                modes.append(mode)

        if len(modes) <= 1:
            modes.append("Auto")

        return modes

    async def async_set_fan_mode(self, fan_mode) -> None:
        """Set new fan mode."""

        value = CLIMATE_AVAILABLE_FAN_MODES[fan_mode]
        gwid = self.device_gwid
        device_id = self.device_id

        await self.client.set_device(gwid, device_id, CLIMATE_FAN_SPEED, value)
        await self.coordinator.async_request_refresh()

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
        await self.coordinator.async_request_refresh()

    @property
    def target_temperature(self) -> int:
        """Return the temperature we try to reach."""
        status = self.get_status(self.coordinator.data)
        return float(status.get(CLIMATE_TARGET_TEMPERATURE, 0))

    async def async_set_temperature(self, **kwargs):
        """ Set new target temperature """
        temp = kwargs.get(ATTR_TEMPERATURE)
        gwid = self.device_gwid
        device_id = self.device_id

        await self.client.set_device(gwid, device_id, CLIMATE_TARGET_TEMPERATURE, int(temp))
        await self.coordinator.async_request_refresh()

    @property
    def current_temperature(self) -> int:
        """Return the current temperature."""
        status = self.get_status(self.coordinator.data)
        return float(status.get(CLIMATE_TEMPERATURE_INDOOR, 0))

    @property
    def min_temp(self) -> int:
        """ Return the minimum temperature """
        rng = self.client.get_range(self.device_gwid, CLIMATE_TARGET_TEMPERATURE)

        return rng.get("Min", CLIMATE_MINIMUM_TEMPERATURE)

    @property
    def max_temp(self) -> int:
        """ Return the maximum temperature """

        rng = self.client.get_range(self.device_gwid, CLIMATE_TARGET_TEMPERATURE)

        return rng.get("Max", CLIMATE_MAXIMUM_TEMPERATURE)

    @property
    def target_temperature_step(self) -> float:
        """ Return temperature step """
        return CLIMATE_TEMPERATURE_STEP