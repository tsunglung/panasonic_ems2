""" Panasonic Smart Home Fan"""
import logging
import asyncio

from homeassistant.components.fan import (
    FanEntityFeature,
    FanEntity
)

from .core.base import PanasonicBaseEntity
from .core.const import (
    DOMAIN,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DEVICE_TYPE_AIRPURIFIER,
    DEVICE_TYPE_FAN,
    DEVICE_TYPE_WASHING_MACHINE,
    FAN_OPERATING_MODE,
    FAN_OSCILLATE,
    FAN_POWER,
    FAN_PRESET_MODES,
    FAN_SPEED,
    AIRPURIFIER_OPERATING_MODE,
    AIRPURIFIER_NANOEX,
    AIRPURIFIER_PRESET_MODES
)

_LOGGER = logging.getLogger(__name__)


PANASONIC_FAN_TYPE = [
    DEVICE_TYPE_AIRPURIFIER,
    DEVICE_TYPE_FAN,
#    DEVICE_TYPE_WASHING_MACHINE
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
    fan = []

    for device_gwid, info in devices.items():
        device_type = int(info.get("DeviceType"))
        if not client.is_supported(info.get("ModelType", "")):
            continue
        for dev in info.get("Information", {}):
            device_id = dev["DeviceID"]
            if device_type in PANASONIC_FAN_TYPE:
                fan.append(
                    PanasonicFan(
                        coordinator,
                        device_gwid,
                        device_id,
                        client,
                        info,
                    )
                )

    async_add_entities(fan, True)

    return True


class PanasonicFan(PanasonicBaseEntity, FanEntity):

    def __init__(
        self,
        coordinator,
        device_gwid,
        device_id,
        client,
        info,
    ):
        super().__init__(coordinator, device_gwid, device_id, client, info)
        device_type = int(info.get("DeviceType", 0))
        self._attr_speed_count = 100
        if device_type == DEVICE_TYPE_FAN:
            self._attr_speed_count = 15
        if device_type == DEVICE_TYPE_AIRPURIFIER:
            self._attr_speed_count = 6
        self._device_type = device_type
        self._state = None

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        feature = FanEntityFeature.SET_SPEED
        status = self.get_status(self.coordinator.data)

        if self._device_type == DEVICE_TYPE_AIRPURIFIER:
            if status.get(AIRPURIFIER_NANOEX, None) is not None:
                feature |= FanEntityFeature.PRESET_MODE

        if self._device_type == DEVICE_TYPE_FAN:
            if status.get(FAN_OPERATING_MODE, None) is not None:
                feature |= FanEntityFeature.PRESET_MODE

            if status.get(FAN_OSCILLATE, None) is not None:
                feature |= FanEntityFeature.OSCILLATE

        if self._device_type == DEVICE_TYPE_WASHING_MACHINE:
            feature |= FanEntityFeature.PRESET_MODE

        return feature

    @property
    def is_on(self):
        """Return true if device is on."""
        status = self.get_status(self.coordinator.data)
#        _LOGGER.error(f"is on {status}")
        self._state = bool(int(status.get(FAN_POWER, 0)))

        return self._state

    @property
    def percentage(self) -> int | None:
        """Return the current speed."""
        status = self.get_status(self.coordinator.data)

        is_on = bool(int(status.get(FAN_POWER, 0)))

        value = 0
        if is_on:
            if status.get(FAN_OPERATING_MODE, None) is None:
                _LOGGER.error("Can not get status!")
                return 0

            if self._device_type == DEVICE_TYPE_FAN:
                value = int(status.get(FAN_SPEED))
            if self._device_type == DEVICE_TYPE_AIRPURIFIER:
                value = int(
                    status.get(AIRPURIFIER_OPERATING_MODE) * self.percentage_step)
            return value
        return value

    async def async_turn_on(
        self,
        speed: str = None,
        percentage: int = None,
        preset_mode: str = None,
        **kwargs,
    ) -> None:
        """Turn the device on."""
        gwid = self.device_gwid
        device_id = self.device_id
        if preset_mode:
            # If operation mode was set the device must not be turned on.
            await self.async_set_preset_mode(preset_mode)
        else:
            await self.client.set_device(self.device, FAN_POWER, 1)
        await asyncio.sleep(1)
        await self.client.update_device(gwid, device_id)
        await self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the device off."""
        gwid = self.device_gwid
        device_id = self.device_id
        await self.client.set_device(self.device, FAN_POWER, 0)
        await asyncio.sleep(1)
        await self.client.update_device(gwid, device_id)
        await self.async_write_ha_state()

    @property
    def preset_modes(self) -> list[str] | None:
        """Get the list of available preset modes."""
        modes = []
        if self._device_type == DEVICE_TYPE_FAN:
            modes = list(FAN_PRESET_MODES.keys())
        if self._device_type == DEVICE_TYPE_AIRPURIFIER:
            for field in self.fields:
                if AIRPURIFIER_NANOEX == field:
                    modes.append(AIRPURIFIER_PRESET_MODES[field])
        return modes

    @property
    def preset_mode(self) -> str | None:
        """Get the current preset mode."""
        preset_mode = None
        status = self.get_status(self.coordinator.data)
        if self._device_type == DEVICE_TYPE_FAN:
            value = status.get(FAN_OPERATING_MODE, 0)
            preset_mode = get_key_from_dict(FAN_PRESET_MODES, value)
        if self._device_type == DEVICE_TYPE_AIRPURIFIER:
            value = status.get(FAN_OPERATING_MODE, 0)
            for key, mode in AIRPURIFIER_PRESET_MODES.items():
                if key in status and status[key]:
                    preset_mode = mode
                    break
        return preset_mode

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode of the fan."""
        gwid = self.device_gwid
        device_id = self.device_id
        if self._device_type == DEVICE_TYPE_FAN:
            await self.client.set_device(
                self.device, FAN_OPERATING_MODE, FAN_PRESET_MODES[preset_mode])
        if self._device_type == DEVICE_TYPE_AIRPURIFIER:
            await self.client.set_device(
                self.device, FAN_OPERATING_MODE, AIRPURIFIER_PRESET_MODES[preset_mode])
        await self.client.update_device(gwid, device_id)
        await self.async_write_ha_state()

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        gwid = self.device_gwid
        device_id = self.device_id
        if percentage == 0:
            await self.client.set_device(self.device, FAN_POWER, 0)
        else:
            if self._device_type == DEVICE_TYPE_FAN:
                await self.client.set_device(self.device, FAN_SPEED, percentage)
            if self._device_type == DEVICE_TYPE_AIRPURIFIER:
                await self.client.set_device(
                    self.device, AIRPURIFIER_OPERATING_MODE, percentage / self.percentage_step)
        await self.client.update_device(gwid, device_id)
        self.async_write_ha_state()

    @property
    def oscillating(self) -> bool | None:
        """Return the oscillation state."""
        status = self.get_status(self.coordinator.data)
        value = False
        if self._device_type == DEVICE_TYPE_FAN:
            value = bool(status.get(FAN_OSCILLATE, 0))

        return value

    async def async_oscillate(self, oscillating: bool) -> None:
        """Set oscillation."""
        gwid = self.device_gwid
        device_id = self.device_id
        if self._device_type == DEVICE_TYPE_FAN:
            await self.client.set_device(self.device, FAN_OSCILLATE, oscillating)
        await self.client.update_device(gwid, device_id)
        self.async_write_ha_state()
