"""the Panasonic Smart Home API."""

from .const import BASE_URL

def open_session():
    url = f"{BASE_URL}/userlogin1"
    return url

def close_session():
    url = f"{BASE_URL}/userlogout1"
    return url

def refresh_token():
    url = f"{BASE_URL}/RefreshToken1"
    return url

def get_user_devices():
    url = f"{BASE_URL}/UserGetRegisteredGwList2"
    return url

def post_device_get_info():
    url = f"{BASE_URL}/DeviceGetInfo"
    return url

def get_device_status():
    url = f"{BASE_URL}/UserGetDeviceStatus"
    return url

def set_device():
    url = f"{BASE_URL}/DeviceSetCommand"
    return url
