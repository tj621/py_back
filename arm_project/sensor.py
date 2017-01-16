#coding=utf-8
__author__ = 'Zxh'

import urllib

def get_sensor_data():
    try:
        url_1 = 'http://121.43.106.119:8020/indoor'
        data = urllib.urlopen(url_1).read()
        return data
    except:
        print 'server connect error'
        return '''
        {
               "1":{
                    "temperature": "26.5",
                    "humidity": "61.2",
                    "radiation": "45",
                    "co2": "381",
                    "update_time": "2016-09-21 09:25:06"
                },
               "2":{
                    "temperature": "27.6",
                    "humidity": "57.2",
                    "radiation": "45",
                    "co2": "390",
                    "update_time": "2016-09-21 09:25:06"
                },
               "3":{
                    "temperature": "27.3",
                    "humidity": "58.6",
                    "radiation": "58",
                    "co2": "311",
                    "update_time": "2016-09-21 09:25:06"
                },
               "4":{
                    "temperature": "25.1",
                    "humidity": "65.2",
                    "radiation": "90",
                    "co2": "398",
                    "update_time": "2016-09-21 09:25:06"
                },
               "5":{
                    "temperature": "26.6",
                    "humidity": "61.3",
                    "radiation": "0",
                    "co2": "0",
                    "update_time": "2016-09-21 09:25:06"
                },
               "6":{
                    "temperature": "26.8",
                    "humidity": "60.8",
                    "radiation": "0",
                    "co2": "0",
                    "update_time": "2016-09-21 09:25:06"
                },
               "7":{
                    "temperature": "26.7",
                    "humidity": "60.5",
                    "radiation": "0",
                    "co2": "0",
                    "update_time": "2016-09-21 09:25:06"
                },
               "8":{
                    "temperature": "27.3",
                    "humidity": "58.7",
                    "radiation": "0",
                    "co2": "0",
                    "update_time": "2016-09-21 09:25:06"
                }
                }
    '''