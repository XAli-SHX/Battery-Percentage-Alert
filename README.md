# Battery Percentage Alert

Get Alerts when laptop charge level is above or below limits - GUI tool for maintaining optimal power level

## Who is this project for?

Most laptop batteries becomes faulty after several years of usage i.e., The charge doesn't decrease gradually. So if the
power source is disconnected, the battery lasts only a few minutes. Without even notifying us, the system will be forced
shutdown leading to interruption in your workflow. This project is meant to be useful for all of us suffering from this
issue.

## What does this project do?

This project throws a notification to the user whenever the charge levels of laptop battery falls below or above the
specified levels. (Useful for maintaining charge at certain levels)

## Features

- Monitor the charge level of your laptop battery
- Notify you when the charge level is low
- Notify you when the battery is sufficiently charged
- Prevent unexpected shutdowns due to low battery
- Control the application with a system tray icon

## Installation

To install the program, simply run the command bellow:

```
pip install -r requirements.txt
```

## How to use

To use this tool, you can simply run the `main_program.pyw` script:

```
pythonw main.pyw
```

### Config

To set the threshold limits that trigger the notifications modify the `config.txt`

```
en 1
max 85
min 25
alert_time_interval 15
```

- `en` sets the alert on or off. If you don't want the notification to alert you, set it to 0
- `max` sets the maximum threshold of battery that is plugged in charger. It will notify you to unplug the charger if
  the battery goes upper-more than that.
- `min` sets the minimum threshold of battery that is unplugged. It will notify you to plug in the charger if
  the battery goes lower than that.
- `alert_time_interval` sets the system checking interval. For example if it's 15, it means that if there is an alert to
  send, it will be sent in every 15 seconds.

## Your Contributions

All your contributions are welcome. If you have an idea for a new feature or have found a bug, please open an issue or
submit a pull request :)
