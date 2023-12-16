""" Panasonic Smart Home Sensor"""
import logging
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity
)

from .core.base import PanasonicBaseEntity
from .core.const import (
    DOMAIN,
    DATA_CLIENT,
    DATA_COORDINATOR,
    SAA_SENSORS,
    DEVICE_TYPE_FRIDGE,
    DEVICE_TYPE_WASHING_MACHINE,
    DEVICE_TYPE_WEIGHT_PLATE,
    WASHING_MACHINE_SENSORS,
    WEIGHT_PLATE_SENSORS,
    PanasonicSensorDescription
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

                for saa, sensors in SAA_SENSORS.items():
                    if device_type == saa:
                        for description in sensors:
                            if description.key in status:
                                entities.extend(
                                    [PanasonicSensor(
                                        coordinator, device_gwid, device_id, client, info, description)]
                                )

            if device_type == DEVICE_TYPE_WASHING_MACHINE:
                for description in WASHING_MACHINE_SENSORS:
                        entities.extend(
                            [PanasonicSensor(
                                coordinator, device_gwid, 1, client, info, description)]
                        )

            if device_type == DEVICE_TYPE_WEIGHT_PLATE:
                for description in WEIGHT_PLATE_SENSORS:
                        entities.extend(
                            [PanasonicSensor(
                                coordinator, device_gwid, 1, client, info, description)]
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


class PanasonicSensor(PanasonicBaseEntity, SensorEntity):
    """Implementation of a Panasonic sensor."""
    entity_description: PanasonicSensorDescription

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
        """Return the name of the sensor."""
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
    def native_value(self):
        """Return the state of the sensor."""
        status = self.get_status(self.coordinator.data)
        if self.entity_description.device_class == SensorDeviceClass.ENUM:
            rng = self.client.get_range(self.device_gwid, self.entity_description.key)
            value = status.get(self.entity_description.key, 0)
            if len(rng) >= 1:
                return get_key_from_dict(rng, int(value))
            return value
        value = status.get(self.entity_description.key, None)
        device_type = int(self.info.get("DeviceType"))
        if device_type != DEVICE_TYPE_FRIDGE:
            if self.entity_description.device_class == SensorDeviceClass.TEMPERATURE:
                if value < -1 or value > 50:
                    return None
        if self.entity_description.device_class == SensorDeviceClass.HUMIDITY:
            if value < 30:
                return None
        if self.entity_description.device_class == SensorDeviceClass.ENERGY:
            if value is not None:
                if isinstance(value, str):
                    value = float(value.replace("-", ""))
                value = float(value * 0.1)
                if value < 1:
                    return None
        return value

#    async def async_update(self):
#        """Fetch state from the device."""
#        await self.coordinator.async_request_refresh()