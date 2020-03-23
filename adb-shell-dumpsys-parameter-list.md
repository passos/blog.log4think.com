---
title: '"adb shell dumpsys" parameter list'
date: '2013-02-20 13:25:19 +0800'
---

# 2013-02-20  '"adb shell dumpsys" parameter list'

Android开发中，常常可以用`adb shell dumpsys`这条命令来dump出系统运行时的状态信息，例如可以这样来察看某个应用的内存使用信息

```text
adb shell dumpsys meminfo com.google.android.apps.maps
```

察看TaskStack

```text
adb shell dumpsys activity activities
```

察看Alarm列表

```text
adb shell dumpsys alarm
```

如果在linux下配合 watch 命令更是可以自动刷新实时察看。这条命令的用法是 `adb shell dumpsys SERVICE [option] [process name]`，可用的SERVICE列表：

```text
$ adb shell dumpsys | grep 'DUMP OF SERVICE' | awk '{print $4}' | tr -d ':'
CustomFrequencyManagerService
DirEncryptService
SYSSCOPE
SecTVOutService
SurfaceFlinger
TvoutService_C
accessibility
account
activity
alarm
apn_settings_policy
application_policy
apppermission_control_policy
appwidget
audio
backup
battery
batteryinfo
bluetooth
bluetooth_a2dp
bluetooth_avrcp
bluetooth_policy
browser_policy
clipboard
clipboardEx
com.orange.authentication.simcard
commontime_management
connectivity
content
country_detector
cpuinfo
date_time_policy
dbinfo
device_info
device_policy
devicestoragemonitor
diskstats
drm.drmManager
dropbox
eas_account_policy
edm_proxy
email_account_policy
email_policy
enterprise_policy
enterprise_vpn_policy
entropy
firewall_policy
gfxinfo
hardware
input
input_method
iphonesubinfo
isms
kioskmode
location
location_policy
lock_settings
mdm.remotedesktop
media.audio_flinger
media.audio_policy
media.camera
media.player
meminfo
mini_mode_app_manager
misc_policy
motion_recognition
mount
netpolicy
netstats
network_management
nfc
notification
package
password_policy
permission
phone
phone_restriction_policy
phoneext
power
remoteinjection
restriction_policy
roaming_policy
samplingprofiler
samsung.facedetection_service
scheduling_policy
search
security_policy
sensorservice
serial
servicediscovery
simphonebook
sip
statusbar
telephony.registry
textservices
throttle
tvoutservice
uimode
updatelock
usagestats
usb
vibrator
voip
vpn_policy
wallpaper
wfd
wifi
wifi_policy
wifip2p
window
```

此外，某些服务还支持如下参数

```text
ACTIVITY MANAGER PENDING INTENTS (adb shell dumpsys activity intents)
ACTIVITY MANAGER BROADCAST STATE (adb shell dumpsys activity broadcasts)
ACTIVITY MANAGER CONTENT PROVIDERS (adb shell dumpsys activity providers)
ACTIVITY MANAGER SERVICES (adb shell dumpsys activity services)
ACTIVITY MANAGER ACTIVITIES (adb shell dumpsys activity activities)
ACTIVITY MANAGER RUNNING PROCESSES (adb shell dumpsys activity processes)
INPUT MANAGER (adb shell dumpsys input)
WINDOW MANAGER LAST ANR (adb shell dumpsys window lastanr)
WINDOW MANAGER POLICY STATE (adb shell dumpsys window policy)
WINDOW MANAGER SESSIONS (adb shell dumpsys window sessions)
WINDOW MANAGER TOKENS (adb shell dumpsys window tokens)
WINDOW MANAGER WINDOWS (adb shell dumpsys window windows)
```

