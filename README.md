[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![Project Maintenance][maintenance-shield]][maintainer]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

# Panda PWR
## Home Assistant Integration

Integrate your [Panda PWR from BIGTREETECH (BTT) | BIQU][pandapwrwiki] with Home Assistant.

[![PandaPWRDevice](https://bttwiki.com/img/PandaPWR/interface.jpg)][pandapwrwiki]


**This integration will set up the following platforms.**

| Platform        | Entity                  | Description                                       |
| --------------- | ----------------------- | ------------------------------------------------- |
| `switch`        | `PowerSwitch`           | Controls the power state of the PandaPWR device.  |
| `switch`        | `UsbSwitch`             | Controls the USB state of the PandaPWR device.    |
| `sensor`        | `CountdownStateSensor`  | Shows the countdown state of the device.          |
| `sensor`        | `AutoPoweroffSensor`    | Displays the auto power-off state.                |
| `sensor`        | `CountdownSensor`       | Shows the countdown timer in seconds.             |
| `sensor`        | `VoltageSensor`         | Measures the voltage (in volts).                  |
| `sensor`        | `CurrentSensor`         | Measures the current (in amperes).                |
| `sensor`        | `PowerSensor`           | Measures the power consumption (in watts).        |
| `sensor`        | `EnergyUsageSensor`     | Tracks energy usage (in kilowatt-hours).          |
| `binary_sensor` | `PowerStateBinarySensor`| Indicates if the power is on or off.              |
| `binary_sensor` | `UsbStateBinarySensor`  | Indicates if the USB port is on or off.           |


## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `HA-Panda-PWR`.
1. Download _all_ the files from the `custom_components/HA-Panda-PWR/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Panda PWR"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[pandapwrwiki]: https://bttwiki.com/Panda%20PWR.html
[buymecoffee]: https://paypal.me/juanillo62gm
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/juanillo62gm/HA-Panda-PWR.svg?style=for-the-badge
[commits]: https://github.com/juanillo62gm/HA-Panda-PWR/commits/main
[license-shield]: https://img.shields.io/github/license/juanillo62gm/HA-Panda-PWR.svg?style=for-the-badge
[maintainer]: https://github.com/juanillo62gm
[maintenance-shield]: https://img.shields.io/badge/maintainer-%20%40juanillo62gm-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/juanillo62gm/HA-Panda-PWR.svg?style=for-the-badge
[releases]: https://github.com/juanillo62gm/HA-Panda-PWR/releases
