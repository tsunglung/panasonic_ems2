[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/tsunglung/panasonic_ems2?style=for-the-badge)
[![GitHub license](https://img.shields.io/github/license/tsunglung/panasonic_ems2?style=for-the-badge)](https://github.com/osk2/panasonic_smart_app/blob/master/LICENSE)

[English](README.md) | [繁體中文](README_zh-tw.md)

# Panasonic IoT TW

Home Assistant 的 Panasonic IoT TW [Android](https://play.google.com/store/apps/details?id=com.panasonic.smart&hl=zh_TW&gl=US&pli=1) [iOS](https://apps.apple.com/tw/app/panasonic-iot-tw/id904484053) 整合套件

本專案修改自  [Osk2's](https://github.com/osk2) [panasonic_smart_app](https://github.com/osk2/panasonic_smart_appp)。
<a href="https://www.buymeacoffee.com/osk2" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 20px !important;width: 70px !important;" ></a>

## 注意

1. 本整合套件僅支援 Panasonic IoT 模組最新版本，請更新 Panasonic IoT 模組的韌體到最新版本。
2. 這套件全新改寫，歡迎回報。目前已支援空調，洗衣機，冰箱，除溼機，全熱交換機和重量感知板。
3. 由於 Panasonic IoT 家電有很多型號，每個型號功能都不一樣，如果遇到問題，歡迎回報問題給我修復問題。

# 安裝

你可以用 [HACS](https://hacs.xyz/) 來安裝這個整合。 步驟如下 custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `tsunglung/panasonic_ems2` > Category: Integration

# 手動安裝

手動複製 `panasonic_ems2` 資料夾到你的 config 資料夾的  `custom_components` 目錄下。

然後重新啟動 Home Assistant.

# 設定

**請使用 Home Assistant 整合設定**

1. 從 GUI. 設定 > 整合 > 新增 整合 > Panasonic Smart IoT
   1. 如果 `Panasonic Smart IoT` 沒有出現在清單裡，請 重新整理 (REFRESH) 網頁。
   2. 如果 `Panasonic Smart IoT` 還是沒有出現在清單裡，請清除瀏覽器的快取 (Cache)。
2. 輸入登入資訊 ([Panasonic Cloud](https://club.panasonic.tw/) 的電子郵件及密碼)
3. 開始使用。

# 協助加入你的 國際版 IoT 智慧家電到 這個自訂整合

如果，你發現你加入整合後，你的智慧家電在 HA 沒有出現或是有實體不正常。很有可能你的國際版 IoT 智慧家電還沒有被支援完整。
你可以協助改善這整合，只要簡單幾個步驟把你的國際版 IoT 智慧家電 家電資訊寄給我除錯。

**方法**

1. 下載並安裝 [Python](https://www.python.org/downloads/)
2. 下載腳本 [panasonic_ems2.py](https://github.com/tsunglung/panasonic_ems2/raw/master/scripts/panasonic_ems2.py) 到你的 Windows 或 MacOS
3. 找到下載的腳本, 並使用 Windows 的 CMD 或是  macOS 的 Terminal, 切換目錄到下載的路徑 "cd [your Download Path]"
4. 執行下載的指令並登入你的 Panasonic Cloud 帳號
```
python panasonic_ems2.py
```
5. 如果登入成功，會有二個檔案產生. 你可以在  "panasonic_devices.json" 找到家電型號資訊，接著把型號資訊以及 "panasonic_commands.json" 提供給我 或是發到 issue.

打賞

|  LINE Pay | LINE Bank | JKao Pay |
| :------------: | :------------: | :------------: |
| <img src="https://github.com/tsunglung/TwANWS/blob/master/linepay.jpg" alt="Line Pay" height="200" width="200">  | <img src="https://github.com/tsunglung/TwANWS/blob/master/linebank.jpg" alt="Line Bank" height="200" width="200">  | <img src="https://github.com/tsunglung/TwANWS/blob/master/jkopay.jpg" alt="JKo Pay" height="200" width="200">  |