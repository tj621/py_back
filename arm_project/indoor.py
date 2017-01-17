# coding=utf-8
from currenttime import get_current_time


class Indoor:
    """the object of indoor climate"""

    def __init__(self, name):
        self.__name = name
        self.__temperature = 5
        self.__humidity = 60
        self.__radiation = 500
        self.__co2 = 400
        self.__update_time = get_current_time()

    def set_name(self,value):
        self.__name=value

    def get_name(self):
        return self.__name

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def set_humidity(self, hum):
        self.__humidity = hum

    def set_update_time(self, value):
        self.__update_time = value

    def set_radiation(self, rad):
        self.__radiation = rad

    def set_co2(self, co2):
        self.__co2 = co2

    def get_update_time(self):
        return self.__update_time

    def get_temperature(self):
        return self.__temperature

    def get_humidity(self):
        return self.__humidity

    def get_radiation(self):
        return self.__radiation

    def get_co2(self):
        return self.__co2

    def build_json(self):
        self.__update_time=get_current_time()
        return '''
        {
           "indoor":{
               "%s":{
                    "temperature": "%s",
                    "humidity": "%s",
                    "radiation": "%s",
                    "co2": "%s",
                    "update_time": "%s"
                }
            }
        }''' \
               % (self.name, self.get_temperature(), self.get_humidity(), self.get_radiation(),
                  self.get_co2(), self.__update_time)

    def save_temp_row(self):
        row = []
        row.append(self.__name)
        row.append(self.__temperature)
        row.append(self.__radiation)
        row.append(self.__co2)
        row.append(self.__update_time)
        return row