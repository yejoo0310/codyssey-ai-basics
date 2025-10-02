import random
import threading
import time
from datetime import datetime


class ParmSensor:
    def __init__(self, name):
        self.name = name
        self.temperature = 0
        self.illuminance_or_light_intensity = 0
        self.humidity = 0

    def set_data(self):
        self.temperature = random.randint(20, 30)
        self.illuminance_or_light_intensity = random.randint(5000, 10000)
        self.humidity = random.randint(40, 70)

    def get_data(self):
        return {
            'temparature': self.temperature,
            'illuminance or Light Intensity': self.illuminance_or_light_intensity,
            'humidity': self.humidity
        }

    def thread_runner(self):
        while True:
            self.set_data()
            data = self.get_data()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(
                f"{current_time} — {self.name}, temp {data['temparature']}, light {data['illuminance or Light Intensity']}, humi {data['humidity']}")
            time.sleep(10)


def main():
    sensors = [
        ParmSensor('Parm1'),
        ParmSensor('Parm2'),
        ParmSensor('Parm3'),
        ParmSensor('Parm4'),
        ParmSensor('Parm5')
    ]

    for sensor in sensors:
        thread = threading.Thread(target=sensor.thread_runner, daemon=True)
        thread.start()

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
