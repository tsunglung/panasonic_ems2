"""Provide info to system health."""

from homeassistant.components import system_health
from homeassistant.core import HomeAssistant, callback

from .core.const import DOMAIN


@callback
def async_register(
    hass: HomeAssistant, register: system_health.SystemHealthRegistration
) -> None:
    # pylint: disable=unused-argument
    """Register system health callbacks."""
    register.async_register_info(system_health_info)


async def system_health_info(hass):
    """Get info for the info page."""
    integration = hass.data["integrations"][DOMAIN]
    data = {"version": f"{integration.version}"}
    data["api_counts"] = hass.data[DOMAIN].get("api_counts", "")
    data["api_counts_per_hour"] = hass.data[DOMAIN].get("api_counts_per_hour", "")

    return data