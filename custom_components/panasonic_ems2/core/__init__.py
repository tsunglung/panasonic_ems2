""" Panasonic Smart Home """
import logging
import asyncio
from http import HTTPStatus
import requests
import json
from datetime import datetime
from typing import Literal

from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.helpers.storage import Store
from homeassistant.const import CONTENT_TYPE_JSON, EVENT_HOMEASSISTANT_STOP

from .exceptions import (
    Ems2TokenNotFound,
    Ems2LoginFailed,
    Ems2ExceedRateLimit,
    Ems2Expectation,
    Ems2TooManyRequest
)
from . import apis
from .const import (
    APP_TOKEN,
    DOMAIN,
    CONF_CPTOKEN,
    CONF_TOKEN_TIMEOUT,
    CONF_REFRESH_TOKEN,
    CONF_REFRESH_TOKEN_TIMEOUT,
    COMMANDS_TYPE,
    CLIMATE_RX_COMMANDS,
    DEVICE_TYPE_FRIDGE,
    FRIDGE_XGS_COMMANDS,
    DEVICE_TYPE_DEHUMIDIFIER,
    WASHING_MACHINE_MODELS,
    WASHING_MACHINE_OPERATING_STATUS,
    DEVICE_TYPE_CLIMATE,
    DEVICE_TYPE_WASHING_MACHINE,
    SET_COMMAND_TYPE,
    CLIMATE_PM25,
    DEHUMIDIFIER_PM25,
    WASHING_MACHINE_PROGRESS,
    FRIDGE_FREEZER_TEMPERATURE,
    FRIDGE_THAW_TEMPERATURE,
    USER_INFO_TYPES,
    DEHUMIDIFIER_MONTHLY_ENERGY,
    FRIDGE_DOOR_OPENS,
    FRIDGE_MONTHLY_ENERGY,
    WASHING_MACHINE_WASH_TIMES,
    WASHING_MACHINE_MONTHLY_ENERGY,
    WASHING_MACHINE_WATER_USED,
    HA_USER_AGENT,
    REQUEST_TIMEOUT
)


_LOGGER = logging.getLogger(__name__)

def api_status(func):
    """
    wrapper_call
    """
    async def wrapper_call(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Ems2TokenNotFound:
            await args[0].refresh_token()
            return await func(*args, **kwargs)
        except Ems2LoginFailed:
            await args[0].login()
            return await func(*args, **kwargs)
        except Ems2TooManyRequest:
            await asyncio.sleep(2)
            return await func(*args, **kwargs)
        except Ems2Expectation:
            return args[0]._devices_info
        except (
            Exception,
        ) as e:
            _LOGGER.warning(f"Got exception {e}")
            #return {}
            return args[0]._devices_info
    return wrapper_call


class PanasonicSmartHome(object):
    """
    Panasonic Smart Home Object
    """
    def __init__(self, hass, session, account, password):
        self.hass = hass
        self.email = account
        self.password = password
        self._session = session
        self._devices = []
        self._commands = []
        self._devices_info = {}
        self._commands_info = {}
        self._cp_token = ""
        self._refresh_token = None
        self._expires_in = 0
        self._expire_time = None
        self._token_timeout = None
        self._refresh_token_timeout = None
        self._mversion = None
        self._update_timestamp = None
        self._api_counts = 0
        self._api_counts_per_hour = 0

    async def request(
        self,
        method: Literal["GET", "POST"],
        headers,
        endpoint: str,
        params=None,
        data=None,
    ):
        """Shared request method"""
        res = {}
        headers["user-agent"] = HA_USER_AGENT
        headers["Content-Type"] = CONTENT_TYPE_JSON

        self._api_counts = self._api_counts + 1
        self._api_counts_per_hour = self._api_counts_per_hour + 1
        try:
            response = await self._session.request(
                method,
                url=endpoint,
                json=data,
                params=params,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
        except requests.exceptions.RequestException:
            _LOGGER.error(f"Failed fetching data for {self.email}")
            return {}
        except Exception as e:
            # request timeout
            _LOGGER.error(f" request exception {e}")
            return {}

        if response.status == HTTPStatus.OK:
            try:
                res = await response.json()
            except:
                res = response.text
        elif response.status == HTTPStatus.BAD_REQUEST:
            raise Ems2ExceedRateLimit
        elif response.status == HTTPStatus.FORBIDDEN:
            raise Ems2LoginFailed
        elif response.status == HTTPStatus.TOO_MANY_REQUESTS:
            raise Ems2TooManyRequest
        elif response.status == HTTPStatus.EXPECTATION_FAILED:
            raise Ems2Expectation
        elif response.status == HTTPStatus.NOT_FOUND:
            _LOGGER.warning(f"Use wrong method or parameters")
            res = {}
        elif response.status == HTTPStatus.METHOD_NOT_ALLOWED:
            _LOGGER.warning(f"The method is not allowed")
            res = {}
        elif response.status == 429:
            _LOGGER.warning(f"Wrong")
            res = {}
        else:
            raise Ems2TokenNotFound

        if isinstance(res, str):
            return {"data": res}

        if isinstance(res, list):
            return {"data": res}

        if isinstance(res, dict):
            return res

        return res

    @property
    def token(self) -> bool:
        if len(self._cp_token) >= 1:
            return True
        return False

    @property
    def devices_number(self) -> int:
        return len(self._devices)

    @api_status
    async def login(self):
        """
        Login to get access token.
        """
        data = {"MemId": self.email, "PW": self.password, "AppToken": APP_TOKEN}
        response = await self.request(
            method="POST", headers={}, data=data, endpoint=apis.open_session()
        )
        self._cp_token = response.get("CPToken", "")
        self._refresh_token = response.get("RefreshToken", "")
        self._token_timeout = response.get("TokenTimeOut", "")
        self._refresh_token_timeout = response.get("RefreshTokenTimeOut", "")
        self._mversion = response.get("MVersion", "")

    @api_status
    async def refresh_token(self):
        """
        refresh access token.
        """
        if self._refresh_token is None:
            raise Ems2LoginFailed

        data = {"RefreshToken": self._refresh_token}
        response = await self.request(
            method="POST", headers={}, data=data, endpoint=apis.refresh_token()
        )
        self._cp_token = response.get("CPToken", "")
        self._refresh_token = response.get("RefreshToken", "")
        self._token_timeout = response.get("TokenTimeOut", "")
        self._refresh_token_timeout = response.get("RefreshTokenTimeOut", "")
        self._mversion = response.get("MVersion", "")

    @api_status
    async def logout(self):
        """
        Logout the account
        """
        data = {}
        await self.request(
            method="POST", headers={}, data=data, endpoint=apis.close_session()
        )

    @api_status
    async def get_user_devices(self):
        """
        List devices that the user has permission
        """

        header = {"CPToken": self._cp_token}
        response = await self.request(
            method="GET", headers=header, endpoint=apis.get_user_devices()
        )
        if isinstance(response, dict):
            self._devices = response.get("GwList", [])
            self._commands = response.get("CommandList", [])

        return self._devices

    @api_status
    async def get_device_ip(self):
        """
        Get the ip of devices
        """
        idx = 0
        header = {"CPToken": self._cp_token}
        for device in self._devices:
            asyncio.sleep(.5)  # avoid to be banned
            gwid = device["GWID"]
            data = {"GWID": gwid}
            response = await self.request(
                method="POST", headers=header, data=data, endpoint=apis.get_gw_ip()
            )
            if isinstance(response, dict):
                self._devices[idx]["GWIP"] = response.get("data", None)
            idx = idx + 1

    def _workaround_info(self, model_type: str, command_type: str, status):
        """
        some workaround on info
        """
        try:
            if ("RX" in model_type and
                    command_type == CLIMATE_PM25 and
                    int(status) == 65535
                ):
                new = -1
            elif (model_type in ["HDH"] and
                    command_type == WASHING_MACHINE_PROGRESS):
                if int(status) >= 19:
                    new = int(status) - 250
                    if new >= 19:
                        new = int(new) - 500
                else:
                    new = int(status)
            elif (model_type in ["XGS"] and
                    command_type in [
                        FRIDGE_FREEZER_TEMPERATURE,
                        FRIDGE_THAW_TEMPERATURE
                    ]
                ):
                new = int(status) - 255
            elif ((model_type in ["GXW", "JHW"]) and
                    command_type == DEHUMIDIFIER_PM25 and
                    int(status) == 65535
                ):
                new = -1
            else:
                new = int(status)
        except:
            new = status
        return new

    def _refactor_info(self, model_type: str, devices_info: list):
        """
        refactor the status of information for easy use
        """
        if len(devices_info) < 1:
            return []

        new = []
        for device in devices_info:
            device_id = device.get("DeviceID", None)
            if device_id is not None:
                device_info = device["Info"]
                device_status = {}
                for info in device_info:
                    command_type = info["CommandType"]
                    status = self._workaround_info(
                        model_type,
                        command_type,
                        info["status"]
                    )
                    device_status[command_type] = status
                device["status"] = device_status
                device.pop("Info", None)
                new.append(device)
        return new

    @api_status
    async def get_device_with_info(self, device: dict, func: list):
        """
        Get device information
        """
        gwid = device["GWID"]
        if not gwid:
            _LOGGER.warning("GWID is not exist!")
            return {}

        header = {
            "CPToken": self._cp_token,
            "auth": device["Auth"],
            "GWID": gwid
        }
        data = []
        for dev in device["Devices"]:
            if dev:
                device_id = dev.get("DeviceID", 1)
                data.append(
                    {"CommandTypes": func, "DeviceID": device_id}
                )
        response = await self.request(
            method="POST", headers=header, data=data, endpoint=apis.post_device_get_info()
        )

        info = []
        if response.get("status", "") == "success":
            info = self._refactor_info(
                self._devices_info[gwid]["ModelType"],
                response["devices"]
            )

        if len(info) >= 1:
            self._devices_info[gwid]["Information"] = info
        return info

    def _get_commands(self, model_type, device_type):
        """
        get commands (saa: service code)
        """
        cmds_list = [
                {"CommandType": "0x00"}
            ]
        if not self._commands:
            return cmds_list
        commands_type = []
        cmds = COMMANDS_TYPE.get(str(device_type), cmds_list)
        if (int(device_type) == DEVICE_TYPE_CLIMATE and
                "RX" in model_type
            ):
            new_cmds = cmds + CLIMATE_RX_COMMANDS
        elif (int(device_type) == DEVICE_TYPE_FRIDGE and
                    "F65" not in model_type
                 ):
            new_cmds = cmds + FRIDGE_XGS_COMMANDS
        else:
            new_cmds = cmds.copy()
        for cmd in new_cmds:
            commands_type.append(
                {"CommandType": cmd}
            )

        return commands_type

    def _refactor_cmds_paras(self, commands_list: list) -> list:
        """
        refactor the status of information for easy use
        """
        new = {}
        cmds_list = []
        for model_type, cmd_list in commands_list.items():
            for cmds in cmd_list:
                lst = cmds["list"]
                cmds_para = {}
                cmds_name = {}
                for cmd in lst:
                    cmd_type = cmd["CommandType"].upper().replace("X", "x")
                    parameters = {}
                    if cmd["ParameterType"] == "enum":
                        parameters_list = cmd["Parameters"]
                        for para in parameters_list:
                            parameters[para[0]] = para[1]
                        if model_type in WASHING_MACHINE_MODELS:
                            if cmd_type == WASHING_MACHINE_OPERATING_STATUS:
                                parameters["Off"] = 0
                    elif "range" in cmd["ParameterType"]:
                        parameters_list = cmd["Parameters"]
                        for para in parameters_list:
                            if "Min" == para[0]:
                                min = para[1] or 0
                            if "Max" == para[0]:
                                max = para[1] or 1
                        if max > 39:
                            parameters[str(min)] = min
                            parameters[str(max)] = max
                        else:
                            for i in range(min, max + 1):
                                parameters[str(i)] = i
                        if cmd["ParameterType"] == "rangeA":
                            parameters["Auto"] = 0
                    cmds_para[cmd_type] = parameters
                    cmds_name[cmd_type] = cmd["CommandName"]
                cmds.pop("list", None)
                cmds["DeviceType"] = str(cmds["DeviceType"])
                cmds["CommandParameters"] = cmds_para
                cmds["CommandName"] = cmds_name
                cmds_list.append(cmds)
            new[model_type] = cmds_list
        self._commands_info = new

    def _offline_info(self, model_type):
        """
        For washing machine, can not get info after offline

        Returns:
            list: the info of device
        """
        commands = COMMANDS_TYPE.get(str(model_type), None)
        status = {}
        if commands:
            for key in commands:
                status[key] = 0

        return [{'DeviceID': 1, 'status': status}]

    def is_supported(self, model_type: str):
        """is model type supported

        Args:
            model_type (str): return True if supported
        """

        return True

    @api_status
    async def get_user_info(self):
        """ get user info

        Returns:
            bool: is user info got
        """
        header = {"CPToken": self._cp_token}
        data = {
            "name": "",
            "from": datetime.today().replace(day=1).strftime("%Y/%m/%d"),
            "unit": "day",
            "max_num": 31,
        }
        for info in USER_INFO_TYPES:
            data["name"] = info
            response = await self.request(
                method="POST", headers=header, data=data, endpoint=apis.get_user_info()
            )

            if "GwList" not in response:
                return False
            for gwinfo in response["GwList"]:
                gwid = gwinfo["GwID"]
                if "Information" not in self._devices_info[gwid]:
                    continue
                device_type = self._devices_info[gwid]["DeviceType"]
                if info == "Other":
                    if device_type == str(DEVICE_TYPE_FRIDGE):
                        self._devices_info[gwid]["Information"][0]["status"][FRIDGE_DOOR_OPENS] = gwinfo["Ref_OpenDoor_Total"]
                    if device_type == str(DEVICE_TYPE_WASHING_MACHINE):
                        self._devices_info[gwid]["Information"][0]["status"][WASHING_MACHINE_WASH_TIMES] = gwinfo["WM_WashTime_Total"]
                        self._devices_info[gwid]["Information"][0]["status"][WASHING_MACHINE_WATER_USED] = gwinfo["WM_WaterUsed_Total"]
                if info == "Power":
                    if device_type == str(DEVICE_TYPE_DEHUMIDIFIER):
                        self._devices_info[gwid]["Information"][0]["status"][DEHUMIDIFIER_MONTHLY_ENERGY] = gwinfo["Total_kwh"]
                    if device_type == str(DEVICE_TYPE_FRIDGE):
                        self._devices_info[gwid]["Information"][0]["status"][FRIDGE_MONTHLY_ENERGY] = gwinfo["Total_kwh"]
                    if device_type == str(DEVICE_TYPE_WASHING_MACHINE):
                        self._devices_info[gwid]["Information"][0]["status"][WASHING_MACHINE_MONTHLY_ENERGY] = gwinfo["Total_kwh"]

        return True

    @api_status
    async def get_devices_with_info(self):
        """
        Get devices information
        """
        devices = await self.get_user_devices()
        for cmd in self._commands:
            self._commands_info[cmd['ModelType']] = cmd["JSON"]
        self._refactor_cmds_paras(self._commands_info)

        await asyncio.sleep(.5)
        header = {"CPToken": self._cp_token}
        response = await self.request(
            method="GET", headers=header, endpoint=apis.get_device_status()
        )

        gwid_status = {}
        if "GwList" in response:
            for dev in response["GwList"]:
                gwid = dev["GWID"]
                status = ""
                for info in dev["List"]:
                    if info.get("CommandType", "") == "0x00":
                        status = info["Status"]
                        break
                    if info.get("CommandType", "") == "0x50": # Washing Machine
                        status = info["Status"]
                        break
                    if info.get("CommandType", "") == "0x65": # Fridge
                        status = info["Status"]
                        break
                gwid_status[gwid] = status

        for device in devices:
            gwid = device["GWID"]
            device_type = device["DeviceType"]
            if gwid not in self._devices_info:
                # _LOGGER.warning(f"gwid not in self._devices_info!")
                self._devices_info[gwid] = device
                gwid_status[gwid] = "force update"
            if len(gwid_status[gwid]) < 1:
                # No status code, it maybe offline or power off of washing machine or network busy
                # _LOGGER.warning(f"gwid {gwid} is offline {self._devices_info[gwid]}!")
                if device_type in [str(DEVICE_TYPE_WASHING_MACHINE)]:
                    self._devices_info[gwid]["Information"] = self._offline_info(device_type)
                continue
            if not self.is_supported(device["ModelType"]):
                continue
            command_types = self._get_commands(
                device["ModelType"],
                device_type
            )
            await asyncio.sleep(.1)
            await self.get_device_with_info(device, command_types)
        await self.get_user_info()
        return self._devices_info

    @api_status
    async def set_device(self, gwid: str, device_id, func: str, value):
        """
        Set device status
        """
        auth = ""

        if "Auth" in self._devices_info[gwid]:
            auth = self._devices_info[gwid]["Auth"]
        if len(auth) <= 1:
            _LOGGER.error(f"There is no auth for {gwid}!")
            return
        device_type = self._devices_info[gwid]["DeviceType"]
        cmd = SET_COMMAND_TYPE[device_type].get(func, None)
        if cmd is None:
            _LOGGER.error(f"There is no cmd for {gwid}!")
            cmd = int(func, 16) + 128

        header = {"CPToken": self._cp_token, "auth": auth}
        param = {"DeviceID": device_id, "CommandType": cmd, "Value": value}

        await self.request(
            method="GET", headers=header, endpoint=apis.set_device(), params=param
        )

    def get_command_name(self, device_gwid:str, command: str) -> str:
        """
        Args:
            device_gwid (str): the gwid of device

        Returns:
            str: the name of command
        """
        if device_gwid not in self._devices_info:
            return None

        model_type = self._devices_info[device_gwid]["ModelType"]
        device_type = self._devices_info[device_gwid]["DeviceType"]
        if model_type not in self._commands_info:
            return None
        cmds_list = self._commands_info[model_type]
        for cmds in cmds_list:
            if device_type == cmds["DeviceType"]:
                cmd_name = cmds.get("CommandName", None)
                if cmd_name:
                    return cmd_name.get(command, None)

        return None

    def get_range(self, device_gwid:str, command: str) -> dict:
        """
        Args:
            device_gwid (str): the gwid of device

        Returns:
            dict: the range dict
        """
        rng = {}
        if device_gwid not in self._devices_info:
            return rng

        model_type = self._devices_info[device_gwid]["ModelType"]
        device_type = self._devices_info[device_gwid]["DeviceType"]
        if model_type not in self._commands_info:
            return rng
        cmds_list = self._commands_info[model_type]
        for cmds in cmds_list:
            if device_type == cmds["DeviceType"]:
                cmd_para = cmds.get("CommandParameters", None)
                if cmd_para:
                    rng = cmd_para.get(command, {})
                    break

        return rng

    async def async_load_tokens(self) -> dict:
        """
        Update tokens in .storage
        """
        default = {
                CONF_CPTOKEN: "",
                CONF_TOKEN_TIMEOUT: "20200101010100",
                CONF_REFRESH_TOKEN: "",
                CONF_REFRESH_TOKEN_TIMEOUT: "20200101010100"
            }
        store = Store(self.hass, 1, f"{DOMAIN}/tokens.json")
        data = await store.async_load() or None
        if not data:
            # force login
            return default
        tokens = data.get(self.email, default)

        # noinspection PyUnusedLocal
        async def stop(*args):
            # save devices data to .storage
            tokens = {
                CONF_CPTOKEN: self._cp_token,
                CONF_TOKEN_TIMEOUT: self._token_timeout,
                CONF_REFRESH_TOKEN: self._refresh_token,
                CONF_REFRESH_TOKEN_TIMEOUT: self._refresh_token_timeout
            }
            data = {
                self.email: tokens
            }
            await store.async_save(data)

        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, stop)
        return tokens

    async def async_store_tokens(self, tokens: dict):
        """
        Update tokens in .storage
        """
        store = Store(self.hass, 1, f"{DOMAIN}/tokens.json")
        data = await store.async_load() or {}
        data = {
            self.email: tokens
        }

        await store.async_save(data)

    @api_status
    async def async_check_tokens(self, tokens=None):
        """
        check token is vaild
        """
        if tokens is None:
            tokens = await self.async_load_tokens()
        cptoken = tokens.get(CONF_CPTOKEN, "")
        token_timeout = tokens.get(
            CONF_TOKEN_TIMEOUT, None)
        refresh_token = tokens.get(CONF_REFRESH_TOKEN, "")
        refresh_token_timeout = tokens.get(
            CONF_REFRESH_TOKEN_TIMEOUT, None)

        if token_timeout is None:
            token_timeout = "20200101010100"
        if refresh_token_timeout is None:
            refresh_token_timeout = "20200101010100"

        now = datetime.now()
        updated_refresh_token = False
        timeout = datetime(
            int(refresh_token_timeout[:4]),
            int(refresh_token_timeout[4:6]),
            int(refresh_token_timeout[6:8]),
            int(refresh_token_timeout[8:10]),
            int(refresh_token_timeout[10:12]),
            int(refresh_token_timeout[12:])
        )

        if (int(timeout.timestamp() - now.timestamp()) < 300):
            # The maximal API access is 10 per hour
            await self.login()

            updated_refresh_token = True
            cptoken = self._cp_token
            token_timeout = self._token_timeout
            refresh_token = self._refresh_token
            refresh_token_timeout = self._refresh_token_timeout
            await self.async_store_tokens({
                CONF_CPTOKEN: cptoken,
                CONF_TOKEN_TIMEOUT: token_timeout,
                CONF_REFRESH_TOKEN: refresh_token,
                CONF_REFRESH_TOKEN_TIMEOUT: refresh_token_timeout,
            })
            self._api_counts_per_hour = 0

        timeout = datetime(
            int(token_timeout[:4]),
            int(token_timeout[4:6]),
            int(token_timeout[6:8]),
            int(token_timeout[8:10]),
            int(token_timeout[10:12]),
            int(token_timeout[12:])
        )

        if ((int(timeout.timestamp() - now.timestamp()) < 300) and
                not updated_refresh_token):
            self._refresh_token = refresh_token
            await self.refresh_token()

            cptoken = self._cp_token
            token_timeout = self._token_timeout
            refresh_token = self._refresh_token
            refresh_token_timeout = self._refresh_token_timeout
            await self.async_store_tokens({
                CONF_CPTOKEN: cptoken,
                CONF_TOKEN_TIMEOUT: token_timeout,
                CONF_REFRESH_TOKEN: refresh_token,
                CONF_REFRESH_TOKEN_TIMEOUT: refresh_token_timeout,
            })
            self._api_counts_per_hour = 0
        else:
            self._cp_token = cptoken
            self._token_timeout = token_timeout
            self._refresh_token = refresh_token
            self._refresh_token_timeout = refresh_token_timeout

        return {
            CONF_CPTOKEN: cptoken,
            CONF_TOKEN_TIMEOUT: token_timeout,
            CONF_REFRESH_TOKEN: refresh_token,
            CONF_REFRESH_TOKEN_TIMEOUT: refresh_token_timeout,
        }

#    @api_status
    async def async_update_data(self):
        """
        Update data
        """
        now = datetime.now()
        self._update_timestamp = now.timestamp()

        await self.async_check_tokens(
            {
                CONF_CPTOKEN: self._cp_token,
                CONF_TOKEN_TIMEOUT: self._token_timeout,
                CONF_REFRESH_TOKEN: self._refresh_token,
                CONF_REFRESH_TOKEN_TIMEOUT: self._refresh_token_timeout,
            }
        )

        try:
            ret = await self.get_devices_with_info()
            self.hass.data[DOMAIN]["api_counts"] = self._api_counts
            self.hass.data[DOMAIN]["api_counts_per_hour"] = self._api_counts_per_hour
            return ret
        except:
            raise UpdateFailed("Failed while updating device status")
