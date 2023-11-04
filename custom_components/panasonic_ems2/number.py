""" Panasonic Smart Home Number"""
import logging
from datetime import timedelta

from homeassistant.components.number import (
    NumberEntity
)

from .core.base import PanasonicBaseEntity
from .core.const import (
    DOMAIN,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DEVICE_TYPE_CLIMATE,
    DEVICE_TYPE_DEHUMIDIFIER,
    CLIMATE_NUMBERS,
    DEHUMIDIFIER_NUMBERS,
    PanasonicNumberDescription
)
SCAN_INTERVAL = timedelta(seconds=60)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities) -> bool:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    devices = coordinator.data

    try:
        entities = []

        for device_gwid, info in devices.items():
            device_type = int(info.get("DeviceType"))
            if not client.is_supported(info.get("ModelType", "")):
                continue
            for dev in info.get("Information", {}):
                device_id = dev["DeviceID"]
                status = dev["status"]

                if device_type == DEVICE_TYPE_CLIMATE:
                    for description in CLIMATE_NUMBERS:
                        if description.key in status:
                            entities.extend(
                                [PanasonicNumber(
                                    coordinator, device_gwid, device_id, client, info, description)]
                            )

                if device_type == DEVICE_TYPE_DEHUMIDIFIER:
                    for description in DEHUMIDIFIER_NUMBERS:
                        if description.key in status:
                            entities.extend(
                                [PanasonicNumber(
                                    coordinator, device_gwid, device_id, client, info, description)]
                            )

        async_add_entities(entities)
    except AttributeError as ex:
        _LOGGER.error(ex)

    return True


def get_key_from_dict(dictionary, value):
    """ get key from dictionary by value"""
    for key, val in dictionary.items():
        if value == val:
            return key
    return None


class PanasonicNumber(PanasonicBaseEntity, NumberEntity):
    """Implementation of a Panasonic number."""
    entity_description: PanasonicNumberDescription

    def __init__(
        self,
        coordinator,
        device_gwid,
        device_id,
        client,
        info,
        description
    ):
        super().__init__(coordinator, device_gwid, device_id, client, info)
        self.entity_description = description
        self._range = client.get_range(device_gwid, self.entity_description.key)

        self._attr_native_min_value = 0
        self._attr_native_max_value = 1

        if self._range:
            self._attr_native_min_value = list(self._range.values())[0]
            self._attr_native_max_value = list(self._range.values())[-1]
        else:
            self._attr_native_min_value = self.entity_description.native_min_value
            self._attr_native_max_value = self.entity_description.native_max_value

    @property
    def name(self):
        """Return the name of the number."""
        name = self.client.get_command_name(self.device_gwid, self.entity_description.key)
        if name is not None:
            return "{} {}".format(
                self.info["NickName"], name
            )
        return "{} {}".format(
            self.info["NickName"], self.entity_description.name
        )

    @property
    def unique_id(self):
        """Return the unique of the number."""
        return "{}_{}_{}".format(
            self.device_gwid,
            self.device_id,
            self.entity_description.key
        )

    @property
    def native_value(self) -> float | None:
        """Return the value reported by the number."""
        status = self.get_status(self.coordinator.data)
        if status:
            value = float(status[self.entity_description.key])
            return value
        return None

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        gwid = self.device_gwid
        device_id = self.device_id

        await self.client.set_device(
            gwid, device_id, self.entity_description.key, int(value))
        await self.coordinator.async_request_refresh()
