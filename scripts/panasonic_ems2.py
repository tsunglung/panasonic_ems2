""" Panasonic Smart Home """
import logging
import asyncio
from http import HTTPStatus
import requests
from getpass import getpass
import ast
import json
from datetime import datetime
from typing import Literal, Final


HA_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
BASE_URL = 'https://ems2.panasonic.com.tw/api'
APP_TOKEN = "D8CBFF4C-2824-4342-B22D-189166FEF503"

CONTENT_TYPE_JSON: Final = "application/json"
REQUEST_TIMEOUT = 15

_LOGGER = logging.getLogger(__name__)


class Ems2BaseException(Exception):
    """ Base exception """


class Ems2TokenNotFound(Ems2BaseException):
    """ Refresh token not found """


class Ems2TokenExpired(Ems2BaseException):
    """ Token expired """


class Ems2InvalidRefreshToken(Ems2BaseException):
    """ Refresh token expired """


class Ems2TooManyRequest(Ems2BaseException):
    """ Too many request """


class Ems2LoginFailed(Ems2BaseException):
    """ Any other login exception """


class Ems2Expectation(Ems2BaseException):
    """ Any other exception """


class Ems2ExceedRateLimit(Ems2BaseException):
    """ API reaches rate limit """

class apis(object):

    def open_session():
        url = f"{BASE_URL}/userlogin1"
        return url

    def get_user_devices():
        url = f"{BASE_URL}/UserGetRegisteredGwList2"
        return url

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
            if self._session:
                response = await self._session.request(
                    method,
                    url=endpoint,
                    json=data,
                    params=params,
                    headers=headers,
                    timeout=REQUEST_TIMEOUT
                )
            else:
                response = requests.request(
                    method,
                    endpoint,
                    params=params,
                    json=data,
                    headers=headers
                )
        except requests.exceptions.RequestException:
            _LOGGER.error(f"Failed fetching data for {self.email}")
            return {}
        except Exception as e:
            # request timeout
            _LOGGER.error(f" request exception {e}")
            return {}

        if self._session:
            if response.status == HTTPStatus.OK:
                try:
                    res = await response.json()
                except:
                    res = {}
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
            else:
                raise Ems2TokenNotFound
        else:
            if response.status_code == HTTPStatus.OK:
                try:
                    res = ast.literal_eval(response.text)
                except Exception as e:
                    res = {}
            elif response.status_code == HTTPStatus.FORBIDDEN:
                print("Login failed, Please check your email or password!")
            elif response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                print("Login too may times, please wait for one hour, then try again")
            elif response.status_code == HTTPStatus.EXPECTATION_FAILED:
                print("Exception, please wait for one hour, then try again")

        if isinstance(res, list):
            return {"data": res}

        return res

    async def login(self):
        """
        Login to get access token.
        """
        data = {"MemId": self.email, "PW": self.password, "AppToken": APP_TOKEN}
        response = await self.request(
            method="POST", headers={}, endpoint=apis.open_session(), data=data
        )
        self._cp_token = response.get("CPToken", "")
        self._refresh_token = response.get("RefreshToken", "")
        self._token_timeout = response.get("TokenTimeOut", "")
        self._refresh_token_timeout = response.get("RefreshTokenTimeOut", "")
        self._mversion = response.get("MVersion", "")

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
        return self._devices, self._commands

    async def get_devices_info(self):
        """
        get devices
        """
        await self.login()
        info = {
            "GwList": [],
            "CommandList": []
        }
        if self._cp_token:
            devices, commands = await self.get_user_devices()
            info["GwList"] = devices
            info["CommandList"] = commands
        else:
            print("Have problem to login, please check your account and password!")
        return info

async def get_devices(username, password):
    client = PanasonicSmartHome(None, None, username, password)

    info = await client.get_devices_info()
    if len(info["GwList"]) >= 1:
        with open("panasonic_devices.json", "w", encoding="utf-8") as f_out:
            f_out.write(json.dumps(info["GwList"], indent=2, ensure_ascii=False))
        with open("panasonic_commands.json", "w", encoding="utf-8") as f_out:
            f_out.write(json.dumps(info["CommandList"], indent=2, ensure_ascii=False))
        print("\nThe panasonic_devices.json and panasonic_commands.json are generated, please send them to the developer!")

##################################################


def main():  # noqa MC0001
    basic_version = "0.0.1"
    print(f"Version: {basic_version}\n")
    username = input("Account: ")
    password = getpass()
    asyncio.run(get_devices(username, password))


if __name__ == '__main__':
    main()
