""" Panasonic Smart Home """
import logging
import asyncio
from datetime import datetime, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .core import PanasonicSmartHome
from .core.const import (
    CONF_UPDATE_INTERVAL,
    DATA_COORDINATOR,
    DATA_CLIENT,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    DOMAINS,
    UPDATE_LISTENER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, hass_config: dict):
    """ setup """
    config = hass_config.get(DOMAIN) or {}

    hass.data[DOMAIN] = {
        'config': config,
    }

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Support Panasonic Smart Home."""

    # migrate data (also after first setup) to options
    if entry.data:
        hass.config_entries.async_update_entry(
            entry, data={}, options=entry.data)
    username = entry.options.get(CONF_USERNAME)
    password = entry.options.get(CONF_PASSWORD)
    session = async_get_clientsession(hass)
    client = PanasonicSmartHome(hass, session, username, password)

    updated_options = entry.options.copy()
    await client.async_check_tokens()

    if not client.token:
        raise ConfigEntryNotReady

    update_interval = entry.options.get(CONF_UPDATE_INTERVAL, None)
    await client.get_user_devices()
    recommand_interval = DEFAULT_UPDATE_INTERVAL
    if isinstance(client.devices_number, int):
        recommand_interval = int(3600 / (150 / (client.devices_number + 1)))
    if update_interval is None:
        # The maximal API access is 150 per hour
        update_interval = recommand_interval
        if update_interval < DEFAULT_UPDATE_INTERVAL:
            update_interval = DEFAULT_UPDATE_INTERVAL
        updated_options[CONF_UPDATE_INTERVAL] = update_interval
    else:
        if (update_interval < recommand_interval or
                update_interval - 24 >= recommand_interval
            ):
            updated_options[CONF_UPDATE_INTERVAL] = recommand_interval

    # await client.get_device_ip()  # disabled because no help
    hass.config_entries.async_update_entry(
        entry=entry,
        options=updated_options,
    )

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"Panasonic Smart Home for {username}",
        update_method=client.async_update_data,
        update_interval=timedelta(seconds=int(update_interval)),
    )

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: client,
        DATA_COORDINATOR: coordinator,
    }

    # init setup for each supported domains
    for domain in DOMAINS:
        hass.async_create_task(hass.config_entries.async_forward_entry_setup(
            entry, domain))

    # add update handler
    if not entry.update_listeners:
        update_listener = entry.add_update_listener(async_update_options)
        hass.data[DOMAIN][entry.entry_id][UPDATE_LISTENER] = update_listener

    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry):
    """ Update Optioins if available """
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """ Unload Entry """
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
#    await client.logout()

    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, domain)
                for domain in DOMAINS
            ]
        )
    )
    if unload_ok:
        update_listener = hass.data[DOMAIN][entry.entry_id][UPDATE_LISTENER]
        update_listener()
        hass.data[DOMAIN].pop(entry.entry_id)
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN)
    return unload_ok


