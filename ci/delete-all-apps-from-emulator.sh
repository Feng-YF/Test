#!/usr/bin/env bash

android_device_port=$(cat $HOME/etc/android_test_device_port)
android_device_port=${android_device_port:-5555} # use default of 5555
$HOME/android/sdk/platform-tools/adb connect 10.0.2.2:$android_device_port

APP_PACKAGES=$($HOME/android/sdk/platform-tools/adb shell pm list packages| grep -E 'hsbc.hsbc|uiautomator2'| cut -d ':' -f2 )
echo "$APP_PACKAGES" | xargs -I % $HOME/android/sdk/platform-tools/adb shell pm uninstall "%"



