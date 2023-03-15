from notifypy import Notify
import psutil
import time


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
                    self.en = bool(value)
                elif key == Const.CONFIG_KEY_MAX:
                    self.max = int(value)
                elif key == Const.CONFIG_KEY_MIN:
                    self.min = int(value)
                elif key == Const.CONFIG_KEY_ALERT_TIME_INTERVAL:
                    self.alertTimeInterval = int(value)
            fp.close()


def sendNotification(title: str, text: str):
    notification = Notify()
    notification.title = "Cool Title"
    notification.message = "Even cooler message."
    notification.send(block=False)


def main():
    config = Config()
    config.readConfig()
    while config.en:
        battery = psutil.sensors_battery()
        isPluggedIn = battery.power_plugged
        if isPluggedIn:
            if int(battery.percent) > int(config.max):
                sendNotification("Unplug charger", ("The Power is at " + str(battery.percent)))
            time.sleep(config.alertTimeInterval)
        else:
            if int(battery.percent) < int(config.min):
                sendNotification("Low Battery, Plug-in charger", ("The Power is at " + str(battery.percent)))

            time.sleep(config.alertTimeInterval)
        config.readConfig()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open("./error.txt", 'w') as fp:
            fp.write(str(e))
            fp.close()
