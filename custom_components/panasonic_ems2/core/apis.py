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

def get_user_info():
    url = f"{BASE_URL}/UserGetInfo"
    return url

def get_update_info():
    url = "https://ems2.panasonic.com.tw/PSHE_MI/api/S3/UpdateCheck"
    return url

def get_user_devices():
    url = f"{BASE_URL}/UserGetRegisteredGwList2"
    return url

def get_gw_ip():
    url = f"{BASE_URL}/UserGetGWIP"
    return url

def post_device_get_info():
    url = f"{BASE_URL}/DeviceGetInfo"
    return url

def get_device_status():
    url = f"{BASE_URL}/UserGetDeviceStatus"
    return url

def get_plate_mode():
    url = f"{BASE_URL}/PlateGetMode"
    return url

def set_device():
    url = f"{BASE_URL}/DeviceSetCommand"
    return url
