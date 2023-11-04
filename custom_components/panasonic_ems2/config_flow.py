"""Config flow to configure Panasonic Samrt Home component."""
from collections import OrderedDict
from typing import Optional
import voluptuous as vol
import asyncio

from homeassistant.config_entries import (
    CONN_CLASS_CLOUD_POLL,
    ConfigFlow,
    OptionsFlow,
    ConfigEntry
)
from homeassistant.const import CONF_USERNAME, CONF_NAME, CONF_PASSWORD
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .core import PanasonicSmartHome
from .core.exceptions import Ems2ExceedRateLimit, Ems2LoginFailed
from .core.const import (
    CONF_UPDATE_INTERVAL,
    CONF_CPTOKEN,
    CONF_TOKEN_TIMEOUT,
    CONF_REFRESH_TOKEN,
    CONF_REFRESH_TOKEN_TIMEOUT,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN
)

class PanasonicSmartHomeFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a Panasonic Samrt Home config flow."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self._username: Optional[str] = None
        self._password: Optional[str] = None
        self._errors: Optional[dict] = {}

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """ get option flow """
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
            self,
            user_input: Optional[ConfigType] = None
    ):  # pylint: disable=arguments-differ
        """Handle a flow initialized by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            self._set_user_input(user_input)
            session = async_get_clientsession(self.hass)

            client = PanasonicSmartHome(
                self.hass,
                session=session,
                account=self._username,
                password=self._password
            )

            try:
                # force login here
                login_info = await client.async_check_tokens()
                self._name = self._username
                if not client.token:
                    raise ConfigEntryNotReady

                await self.async_set_unique_id(self._username)

                await asyncio.sleep(1)  # add sleep 1 to avoid frequency request
                devices = await client.get_user_devices()
                if len(devices) < 1:
                    self._errors["status"] = "error"
                    self._errors["base"] = "network_busy"
                    raise ConfigEntryNotReady

                login_info[CONF_USERNAME] = self._username
                login_info[CONF_PASSWORD] = self._password
                return self._async_get_entry(login_info)
            except Ems2ExceedRateLimit:
                self._errors["base"] = "rate_limit"
            except Ems2LoginFailed:
                self._errors["base"] = "auth"
            except:
                self._errors["status"] = "error"
                self._errors["base"] = "connection_error"

        fields = OrderedDict()
        fields[vol.Required(CONF_USERNAME,
                            default=self._username or vol.UNDEFINED)] = str
        fields[vol.Required(CONF_PASSWORD,
                            default=self._password or vol.UNDEFINED)] = str

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(fields),
            errors=self._errors
        )

    @property
    def _name(self):
        # pylint: disable=no-member
        # https://github.com/PyCQA/pylint/issues/3167
        return self.context.get(CONF_NAME)

    @_name.setter
    def _name(self, value):
        # pylint: disable=no-member
        # https://github.com/PyCQA/pylint/issues/3167
        self.context[CONF_NAME] = value
        self.context["title_placeholders"] = {"name": self._name}

    def _set_user_input(self, user_input):
        if user_input is None:
            return
        self._username = user_input.get(CONF_USERNAME, "")
        self._password = user_input.get(CONF_PASSWORD, "")

    @callback
    def _async_get_entry(self, login_info: dict):
        return self.async_create_entry(
            title=self._name,
            data=login_info,
        )


class OptionsFlowHandler(OptionsFlow):
    # pylint: disable=too-few-public-methods
    """Handle options flow changes."""
    _username = None
    _password = None
    _update_interval = 600

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            if len(user_input.get(CONF_USERNAME, "")) >= 1:
                self._username = user_input.get(CONF_USERNAME)
            if len(user_input.get(CONF_PASSWORD, "")) >= 1:
                self._password = user_input.get(CONF_PASSWORD)

            self._password = user_input.get(
                CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)

            return self.async_create_entry(
                title=self._username,
                data={
                    CONF_USERNAME: self._username,
                    CONF_PASSWORD: self._password,
                    CONF_UPDATE_INTERVAL: self._update_interval,
                },
            )
        self._username = self.config_entry.options[CONF_USERNAME]
        self._password = self.config_entry.options.get(CONF_PASSWORD, '')
        self._update_interval = self.config_entry.options.get(
            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_UPDATE_INTERVAL, default=self.config_entry.options.get(
                        CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                    )): vol.All(
                        vol.Coerce(int), vol.Range(
                            min=DEFAULT_UPDATE_INTERVAL, max=600)
                    )
                }
            ),
        )
