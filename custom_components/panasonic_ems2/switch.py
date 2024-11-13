""" Panasonic Smart Home Switch"""
import logging
import asyncio
from datetime import timedelta

from homeassistant.components.switch import (
    SwitchEntity
)
from homeassistant.const import STATE_UNAVAILABLE

from .core.base import PanasonicBaseEntity
from .core.const import (
    DOMAIN,
    DATA_CLIENT,
    DATA_COORDINATOR,
    DEVICE_TYPE_LIGHT,
    DEVICE_TYPE_WASHING_MACHINE,
    LIGHT_POWER,
    LIGHT_OPERATION_STATE,
    WASHING_MACHINE_SWITCHES,
    SAA_SWITCHES,
    PanasonicSwitchDescription
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

                for saa, switchs in SAA_SWITCHES.items():
                    if device_type == saa:
                        for description in switchs:
                            if description.key in status:
                                entities.extend(
                                    [PanasonicSwitch(
                                        coordinator, device_gwid, device_id, client, info, description)]
                                )

            if device_type == DEVICE_TYPE_WASHING_MACHINE:
                for description in WASHING_MACHINE_SWITCHES:
                    if True:
                        entities.extend(
                            [PanasonicSwitch(
                                coordinator, device_gwid, 1, client, info, description)]
                        )

        async_add_entities(entities)
    except AttributeError as ex:
        _LOGGER.error(ex)

    return True


class PanasonicSwitch(PanasonicBaseEntity, SwitchEntity):
    """Implementation of a Panasonic switch."""
    entity_description: PanasonicSwitchDescription

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
        """Return the name of the switch."""
        name = self.client.get_command_name(self.device_gwid, self.entity_description.key)

        if name is not None:
            # hard code
            if "nanoe" in name:
                return "{} {}".format(
                    self.info["NickName"], self.entity_description.name
                )
            device_name = ""
            for dev in self.info.get("Devices", {}):
                if self.device_id == dev.get("DeviceID", 0):
                    device_name = dev.get("Name", "")
                    break

            return "{} {}{}".format(
                self.info["NickName"], device_name, name
            )
        return "{} {}".format(
            self.info["NickName"], self.entity_description.name
        )

    @property
    def unique_id(self):
        """Return the unique of the switch."""
        return "{}_{}_{}".format(
            self.device_gwid,
            self.device_id,
            self.entity_description.key
        )

    @property
    def is_on(self) -> int:
        device_id = self.device_id
        info = self.coordinator.data
        status = self.get_status(info)

        avaiable = status.get(self.entity_description.key, None)
        if avaiable is None:
            return STATE_UNAVAILABLE

        if ((int(info[self.device_gwid].get("DeviceType")) == DEVICE_TYPE_LIGHT) and
                (self.entity_description.key == LIGHT_POWER)):
            for device in info[self.device_gwid]["Information"]:
                operation_state = device["status"].get(LIGHT_OPERATION_STATE, None)
                if operation_state != None:
                    state = (int(operation_state) & (1 << (device_id - 1))) >> (device_id - 1)
                    return bool(state)
            return STATE_UNAVAILABLE

        state = status.get(self.entity_description.key)
        if not isinstance(state, int):
            return STATE_UNAVAILABLE
        return bool(int(status.get(self.entity_description.key, 0)))

    async def async_turn_on(self) -> None:
        gwid = self.device_gwid
        device_id = self.device_id
        await self.client.set_device(gwid, device_id, self.entity_description.key, 1)
        await asyncio.sleep(1)
        await self.client.update_device(gwid, device_id)
        self.async_write_ha_state()

    async def async_turn_off(self) -> None:
        gwid = self.device_gwid
        device_id = self.device_id
        await self.client.set_device(gwid, device_id, self.entity_description.key, 0)
        await asyncio.sleep(1)
        await self.client.update_device(gwid, device_id)
        self.async_write_ha_state()
