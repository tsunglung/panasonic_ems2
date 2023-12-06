""" Panasonic Smart Home Binary Sensor"""
import logging
from datetime import timedelta

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity
)

from .core.base import PanasonicBaseEntity
from .core.const import (
    DOMAIN,
    DATA_CLIENT,
    DATA_COORDINATOR,
    SAA_BINARY_SENSORS,
    PanasonicBinarySensorDescription
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

                for saa, sensors in SAA_BINARY_SENSORS.items():
                    if device_type == saa:
                        for description in sensors:
                            if description.key in status:
                                entities.extend(
                                    [PanasonicBinarySensor(
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


class PanasonicBinarySensor(PanasonicBaseEntity, BinarySensorEntity):
    """Implementation of a Panasonic binary sensor."""
    entity_description: PanasonicBinarySensorDescription

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

    @property
    def name(self):
        """Return the name of the binary sensor."""
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
        """Return the unique of the sensor."""
        return "{}_{}_{}".format(
            self.device_gwid,
            self.device_id,
            self.entity_description.key
        )

    @property
    def is_on(self) -> bool:
        """Return the state of the binary sensor."""
        status = self.get_status(self.coordinator.data)
        value = status.get(self.entity_description.key, False)
        return value
