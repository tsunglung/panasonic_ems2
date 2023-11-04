""" Panasonic Smart Home Fan"""
import logging
import asyncio

from homeassistant.components.humidifier import (
    HumidifierDeviceClass,
    HumidifierEntityFeature,
    HumidifierEntity
)

from .core.base import PanasonicBaseEntity
from .core.const import (
    DOMAIN,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DEVICE_TYPE_DEHUMIDIFIER,
    DEHUMIDIFIER_DEFAULT_MODES,
    DEHUMIDIFIER_POWER,
    DEHUMIDIFIER_MODE,
    DEHUMIDIFIER_TARGET_HUMIDITY,
    DEHUMIDIFIER_MAX_HUMIDITY,
    DEHUMIDIFIER_MIN_HUMIDITY
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
    humidifer = []

    for device_gwid, info in devices.items():
        device_type = int(info.get("DeviceType"))
        if not client.is_supported(info.get("ModelType", "")):
            continue
        for dev in info.get("Information", {}):
            device_id = dev["DeviceID"]
            if device_type == DEVICE_TYPE_DEHUMIDIFIER:
                humidifer.append(
                    PanasonicHumidifier(
                        coordinator,
                        device_gwid,
                        device_id,
                        client,
                        info,
                    )
                )

    async_add_entities(humidifer, True)

    return True

def get_key_from_dict(dictionary, value):
    """ get key from dictionary by value"""
    for key, val in dictionary.items():
        if value == val:
            return key
    return None


class PanasonicHumidifier(PanasonicBaseEntity, HumidifierEntity):

    _attr_supported_features = HumidifierEntityFeature.MODES
    _attr_device_class = HumidifierDeviceClass.HUMIDIFIER

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
        self._device_type = device_type
        self._modes = {}
        self._state = None

        rng = client.get_range(device_gwid, DEHUMIDIFIER_TARGET_HUMIDITY)

        try:
            self._attr_min_humidity = int(list(rng.keys())[0].replace("%", ""))
        except:
            self._attr_min_humidity = DEHUMIDIFIER_MIN_HUMIDITY
        try:
            self._attr_max_humidity = int(list(rng.keys())[-1].replace("%", ""))
        except:
            self._attr_max_humidity = DEHUMIDIFIER_MAX_HUMIDITY

    @property
    def available_modes(self) -> list:
        """Return a list of available modes.

        Requires HumidifierEntityFeature.MODES.
        """
        rng = self.client.get_range(self.device_gwid, DEHUMIDIFIER_MODE)
        if len(rng) >= 1:
            self._modes = rng
            return list(rng.keys())
        self._modes = DEHUMIDIFIER_DEFAULT_MODES
        return list(DEHUMIDIFIER_DEFAULT_MODES.keys())

    @property
    def mode(self) -> str | None:
        """Return the current mode, e.g., home, auto, baby.

        Requires HumidifierEntityFeature.MODES.
        """
        status = self.get_status(self.coordinator.data)
        if status:
            value = int(status[DEHUMIDIFIER_MODE])
            return get_key_from_dict(self._modes, value)
        return None

    @property
    def is_on(self):
        """Return true if device is on."""
        status = self.get_status(self.coordinator.data)
#        _LOGGER.error(f"is on {status}")
        self._state = bool(int(status.get(DEHUMIDIFIER_POWER, 0)))

        return self._state

    @property
    def target_humidity(self) -> int:
        status = self.get_status(self.coordinator.data)
        if status:
            try:
                value = int(status[DEHUMIDIFIER_TARGET_HUMIDITY])
                return value
            except:
                return None
        return None

    async def async_set_humidity(self, humidity: int) -> None:
        """Set new target humidity."""
        gwid = self.device_gwid
        device_id = self.device_id

        await self.client.set_device(gwid, device_id, DEHUMIDIFIER_TARGET_HUMIDITY, humidity)
        await self.coordinator.async_request_refresh()

    async def async_set_mode(self, mode: str) -> None:
        """Set new mode."""
        gwid = self.device_gwid
        device_id = self.device_id

        value = self._modes[mode]

        await self.client.set_device(gwid, device_id, DEHUMIDIFIER_MODE, value)
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self) -> None:
        """Turn the device on."""
        gwid = self.device_gwid
        device_id = self.device_id

        await self.client.set_device(gwid, device_id, DEHUMIDIFIER_POWER, 1)
        await asyncio.sleep(1)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """Turn the device off."""
        gwid = self.device_gwid
        device_id = self.device_id

        await self.client.set_device(gwid, device_id, DEHUMIDIFIER_POWER, 0)
        await asyncio.sleep(1)
        await self.coordinator.async_request_refresh()
