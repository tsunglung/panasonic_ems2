""" Panasonic Smart Home Select"""
import logging
from datetime import timedelta

from homeassistant.components.select import (
    SelectEntity
)

from .core.base import PanasonicBaseEntity
from .core.const import (
    DOMAIN,
    DATA_CLIENT,
    DATA_COORDINATOR,
    SAA_SELECTS,
    DEVICE_TYPE_WASHING_MACHINE,
    WASHING_MACHINE_SELECTS,
    PanasonicSelectDescription
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

                for saa, selects in SAA_SELECTS.items():
                    if device_type == saa:
                        for description in selects:
                            if description.key in status:
                                entities.extend(
                                    [PanasonicSelect(
                                        coordinator, device_gwid, device_id, client, info, description)]
                                )

            if device_type == DEVICE_TYPE_WASHING_MACHINE:
                for description in WASHING_MACHINE_SELECTS:
                        entities.extend(
                            [PanasonicSelect(
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


class PanasonicSelect(PanasonicBaseEntity, SelectEntity):
    """Implementation of a Panasonic select."""
    entity_description: PanasonicSelectDescription

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
        self._range = []

    @property
    def name(self):
        """Return the name of the select."""
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
        """Return the unique of the select."""
        return "{}_{}_{}".format(
            self.device_gwid,
            self.device_id,
            self.entity_description.key
        )

    @property
    def options(self) -> list:
        """Return a set of selectable options."""
        rng = self.client.get_range(self.device_gwid, self.entity_description.key)
        if len(rng) >= 1:
            self._range = rng
            return list(rng.keys())
        for idx in range(len(self.entity_description.options)):
            option = self.entity_description.options[idx]
            self._range[option] = self.entity_description.options_value.index(idx)
        return self.entity_description.options

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        status = self.get_status(self.coordinator.data)
        if status:
            value = int(status[self.entity_description.key])
            return get_key_from_dict(self._range, value)
        return None

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        value = self._range[option]
        gwid = self.device_gwid
        device_id = self.device_id

        await self.client.set_device(
            gwid, device_id, self.entity_description.key, int(value))
        await self.client.update_device(gwid, device_id)
        self.async_write_ha_state()
