[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/tsunglung/panasonic_ems2?style=for-the-badge)
[![GitHub license](https://img.shields.io/github/license/tsunglung/panasonic_ems2?style=for-the-badge)](https://github.com/osk2/panasonic_smart_app/blob/master/LICENSE)


[繁體中文](README_zh-tw.md) | [English](README.md)

# Panasonic IoT TW

Home Assistant integration for Panasonic IoT TW [Android](https://play.google.com/store/apps/details?id=com.panasonic.smart&hl=zh_TW&gl=US&pli=1) [iOS](https://apps.apple.com/tw/app/panasonic-iot-tw/id904484053).

This integration allows you to control your Panasonic IoT appliances.

This project is forked from [Osk2's](https://github.com/osk2) [panasonic_smart_app](https://github.com/osk2/panasonic_smart_appp).
<a href="https://www.buymeacoffee.com/osk2" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 20px !important;width: 70px !important;" ></a>

## Note

1. This integration only support the latest version of Panasonic IoT module, please use the latest version of IoT module.
2. The code was refacotred, so it is still in draft and currently only support Clmate, Washing Machine, Fridge and Dehumidifier.

# Installation

You can install component with [HACS](https://hacs.xyz/) custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `tsunglung/panasonic_ems2` > Category: Integration

Then restart Home Assistant.

### Manually Installation

Copy `panasonic_ems2` folder of custom_components in this repository to `custom_components` folder in your config folder.

# Configuration

**Please use the config flow of Home Assistant**

1. With GUI. Configuration > Integration > Add Integration > `Panasonic Smart IoT`
   1. If the integration didn't show up in the list please REFRESH the page
   2. If the integration is still not in the list, you need to clear the browser cache.
2. Enter the Login info (email and password of [Panasonic Cloud](https://club.panasonic.tw/))
3. Enjoy

Buy Me A Coffee

|  LINE Pay | LINE Bank | JKao Pay |
| :------------: | :------------: | :------------: |
| <img src="https://github.com/tsunglung/TwANWS/blob/master/linepay.jpg" alt="Line Pay" height="200" width="200">  | <img src="https://github.com/tsunglung/TwANWS/blob/master/linebank.jpg" alt="Line Bank" height="200" width="200">  | <img src="https://github.com/tsunglung/TwANWS/blob/master/jkopay.jpg" alt="JKo Pay" height="200" width="200">  |
