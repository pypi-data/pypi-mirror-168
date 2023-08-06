# Overview

ESP32-S2/S3 can support up to 14 capacitive touch sensor, which can be used to design touch buttons, sliders, etc. For a long time touchpad (touchsensor) debugging and driver configuration has been a difficult problem. But now we're trying to make it easier and interesting, now several touchpad debugging tools and methods for ESP chip is under developing.

We've made some progress so far, and would like to sharing a Beta version of our touchpad debugging tool (tptool) with you. This version support:

1. Modification of all Touch parameters in real time, including thresholds, filter parameters, and more.
2. Plot all Touch channel's data (raw, smooth, baseline, diff) in real time,
3. Control and log hardware events in table
4. Enter sleep mode with one button, the wakeup channel parameters can be configured
5. Wireless debugging, using ESP-NOW protocol (A second ESP32XX module is required as a receiver)
6. Save the original data on the local machine for further analysis
7. More...

If you're interested, please try it. (There could be some issues in current Beta version, if you encounter any problems, feel free to add your questions to https://esp32.com/

## How to run the GUI

1. Install from pip using `pip install tptool`
2. Run GUI using `python -m tptool`

![tptool main window](https://esp32.com/download/file.php?id=9720)

## Note

Currently supported SoC:

* ESP32-S2
* ESP32-S3

Currently only supports using the [Debug Firmware](https://esp32.com/download/file.php?id=10060) for touchsensor debugging, please using any ESP download tool then following the below configuration for download.

* [Debug Firmware](https://esp32.com/download/file.php?id=10060)
* User guide: [ESP_TouchSensor_Debugging_Tool(Beta).pdf](https://esp32.com/download/file.php?id=9725)
