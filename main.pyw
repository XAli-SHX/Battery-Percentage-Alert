from notifypy import Notify
import psutil
import time
import pystray
from PIL import Image
import os


class Const:
    CONFIG_FILE_PATH = "./config.txt"
    APP_DEFAULT_ENABLE = True
    APP_DEFAULT_ALERT_TIME_INTERVAL = 15
    BATTERY_DEFAULT_MIN = 25
    BATTERY_DEFAULT_MAX = 85
    CONFIG_KEY_EN = "en"
    CONFIG_KEY_MAX = "max"
    CONFIG_KEY_MIN = "min"
    CONFIG_KEY_ALERT_TIME_INTERVAL = "alert_time_interval"

    STRAY_ENABLE = "Enable"
    STRAY_DISABLE = "Disable"
    STRAY_OPEN_CONFIG = "Open config.txt"
    STRAY_EXIT = "Exit"


class Config:
    en: bool
    min: int
    max: int
    alertTimeInterval: int
    configPath: str

    def __init__(self):
        self.configPath = Const.CONFIG_FILE_PATH
        self.en = Const.APP_DEFAULT_ENABLE
        self.min = Const.BATTERY_DEFAULT_MIN
        self.max = Const.BATTERY_DEFAULT_MAX
        self.alertTimeInterval = Const.APP_DEFAULT_ALERT_TIME_INTERVAL
        self.readConfig()

    def readConfig(self):
        with open(self.configPath, 'r') as fp:
            for line in fp.readlines():
                line = line.strip()
                if line == "":
                    continue
                key, value = line.split()
                if key == Const.CONFIG_KEY_EN:
                    self.en = int(value) == 1
                elif key == Const.CONFIG_KEY_MAX:
                    self.max = int(value)
                elif key == Const.CONFIG_KEY_MIN:
                    self.min = int(value)
                elif key == Const.CONFIG_KEY_ALERT_TIME_INTERVAL:
                    self.alertTimeInterval = int(value)
            fp.close()

    def writeConfig(self):
        en = 0
        if self.en:
            en = 1
        with open(self.configPath, 'w') as fp:
            fp.write(f"{Const.CONFIG_KEY_EN} {en}\n")
            fp.write(f"{Const.CONFIG_KEY_MAX} {self.max}\n")
            fp.write(f"{Const.CONFIG_KEY_MIN} {self.min}\n")
            fp.write(f"{Const.CONFIG_KEY_ALERT_TIME_INTERVAL} {self.alertTimeInterval}")
            fp.close()


def sendNotification(title: str, text: str):
    notification = Notify()
    notification.title = title
    notification.message = text
    notification.send(block=False)


def onIconRightClicked(stray, query):
    query = str(query)
    config = Config()
    if query == Const.STRAY_ENABLE:
        config.en = True
        sendNotification("Alert Enabled", "You can turn it off from the system tray icon.")
    elif query == Const.STRAY_DISABLE:
        config.en = False
        sendNotification("Alert Disabled", "You can turn it on from the system tray icon.")
    elif query == Const.STRAY_OPEN_CONFIG:
        openConfigFile()
    elif query == Const.STRAY_EXIT:
        config.en = False
        config.writeConfig()
        stray.stop()
        exit(0)
    config.writeConfig()


# left click on icon is currently not supported by pystray library
def onIconLeftClicked(icon, item):
    openConfigFile()


def openConfigFile():
    os.startfile(str(os.path.dirname(os.path.abspath(__file__))) + '\\config.txt')


def setupStray():
    image = Image.open("./assets/icon.png")
    stray = pystray.Icon("Battery-Percentage-Alert", image,
                         "Battery-Percentage-Alert",
                         menu=pystray.Menu(
                             pystray.MenuItem(Const.STRAY_ENABLE, onIconRightClicked),
                             pystray.MenuItem(Const.STRAY_DISABLE, onIconRightClicked),
                             pystray.MenuItem(Const.STRAY_OPEN_CONFIG, onIconRightClicked),
                             pystray.MenuItem(Const.STRAY_EXIT, onIconRightClicked)))
    stray.run()


def main():
    config = Config()
    showSystemStatus(config)
    while True:
        battery = psutil.sensors_battery()
        isPluggedIn = battery.power_plugged
        if isPluggedIn:
            if int(battery.percent) > int(config.max) and config.en:
                sendNotification("Unplug charger", ("The Power is at " + str(battery.percent)))
        else:
            if int(battery.percent) < int(config.min) and config.en:
                sendNotification("Low Battery, Plug-in charger", ("The Power is at " + str(battery.percent)))
        time.sleep(config.alertTimeInterval)
        config.readConfig()


def showSystemStatus(config: Config):
    if config.en:
        sendNotification("Battery Percentage Alert", "Alert is enable")
    else:
        sendNotification("Battery Percentage Alert", "Alert is disable")


if __name__ == "__main__":
    try:
        setupStray()
        main()
    except Exception as e:
        with open("./error.txt", 'w') as errorFile:
            errorFile.write(str(e))
            errorFile.close()
