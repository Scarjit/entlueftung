import math
import threading
import time

import adafruit_dht
import board


# https://journals.ametsoc.org/view/journals/apme/35/4/1520-0450_1996_035_0601_imfaos_2_0_co_2.xml
def get_dew_point_c(t_air_c, rel_humidity) -> float:
    A = 17.27
    B = 237.7
    alpha = ((A * t_air_c) / (B + t_air_c)) + math.log(rel_humidity / 100.0)
    return (B * alpha) / (A - alpha)


class DHT:
    last_temperature_c: float = 0
    last_humidity_p: float = 0
    last_dew_point_c: float = 0
    last_successful_read_time: float = 0

    def __init__(self):
        self.dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        # spawn reader thread
        threading.Thread(target=self.read).start()

    def get_last_temperature_c(self) -> float:
        return self.last_temperature_c

    def get_last_humidity_p(self) -> float:
        return self.last_humidity_p

    def get_last_dew_point_c(self) -> float:
        return self.last_dew_point_c

    def get_last_successful_read_time(self) -> float:
        return self.last_successful_read_time

    def read(self):
        while True:
            try:
                # Print the values to the serial port
                temperature_c = self.dhtDevice.temperature
                humidity = self.dhtDevice.humidity
                dew_point_c = get_dew_point_c(temperature_c, humidity)
                print(
                    "Temp: {:.1f} C    Humidity: {}%    Dew Point: {:.1f} C".format(
                        temperature_c, humidity, dew_point_c
                    )
                )
                self.last_temperature_c = temperature_c
                self.last_humidity_p = humidity
                self.last_dew_point_c = dew_point_c
                self.last_successful_read_time = time.time()

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                self.dhtDevice.exit()
                exit(1)

            time.sleep(2.0)
