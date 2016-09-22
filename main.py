# coding=utf-8

from currenttime import get_current_time
from flask import Flask, request
from outdoor import Outdoor
from control import Control
from indoor import Indoor
from scheduler import Scheduler
from parameter import Parameter
from database import save_db_indoor, save_db_outdoor, save_db_control, get_db_parameter, save_db_parameter, \
    get_db_indoor, get_db_outdoor
from autorun import auto_run_main, get_side_wait_time
import json
import urllib
import requests
import sensor


r = requests
app = Flask(__name__)

node0 = Indoor('1')
outdoor = Outdoor()
c = Control()
p = Parameter()

control_method = "computer"
isConnect = False
url = "http://127.0.0.1:8050/"
start_time = get_current_time()
indoor_node_data=''''''

def server_connect():
    global isConnect, start_time
    try:
        data = urllib.urlopen(url).read()
        if data == 'success':
            isConnect = True
        print 'server connect'
    except:
        start_time = get_current_time()
        isConnect = False
        print 'server disconnect'


def post_server_data():
    global isConnect
    if isConnect:
        try:
            url_indoor = url + 'indoor'
            post_data = get_db_indoor(start_time)
            r.post(url_indoor, post_data)
        except:
            print 'post indoor data fail, please review'
        try:
            url_outdoor = url + 'outdoor'
            post_data = get_db_outdoor(start_time)
            r.post(url_outdoor, post_data)
        except:
            print 'post indoor data fail, please review'


def get_web_command():
    global isConnect
    if isConnect:
        url_1 = url + 'webControl'
        data = urllib.urlopen(url_1).read()
        if data != 'wait':
            c.handle_post(data)


def update_indoor():
    global start_time,indoor_node_data,ind
    indoor_node_data=sensor.get_sensor_data()
    if isConnect == True:
        start_time = get_current_time()
    obj=json.loads(indoor_node_data)
    for key in obj.keys():
        node0.set_name(key)
        value=obj.get(key)
        node0.set_update_time(value['update_time'])
        node0.set_co2(value['co2'])
        node0.set_temperature(value['temperature'])
        node0.set_humidity(value['humidity'])
        save_db_indoor(node0)
    print 'indoor updated', get_current_time()


def update_outdoor():
    try:
        outdoor.get_weather_from_api()
        outdoor.set_wind_direction_number()
    except:
        print 'get outdoor from weather api error'
    outdoor.set_update_time(get_current_time())
    save_db_outdoor(outdoor)
    print 'outdoor updated', get_current_time()


def update_control():
    # save_db_control(c)
    print 'control updated', get_current_time()


def auto_running():
    global node0, c, outdoor, p
    auto_run_main(node0, outdoor, c, p)


auto = Scheduler(900, auto_running)
wait_time = Scheduler(1, get_side_wait_time)


@app.route('/indoor')
def get_indoor():
    return indoor_node_data


@app.route('/outdoor')
def response_outdoor():
    return outdoor.build_json()


@app.route('/control', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        try:
            data = request.data
            c.set_update_time(get_current_time())
            r=c.handle_post(data)
            save_db_control(r)
            return r
        except ValueError:
            return "get currently control state success"
    else:
        return c.build_json()


@app.route('/auto', methods=['GET', 'POST'])
def auto_run():
    global control_method
    if request.method == 'POST':
        data = request.data
        obj = json.loads(data)
        model = obj['model']
        if model == 'auto':
            if control_method != 'auto':
                auto_running()
                get_side_wait_time()
                wait_time.start()
                auto.start()
        else:
            if control_method == 'auto':
                auto.stop()
                wait_time.stop()
        control_method = model
        return model
    else:
        return 'get request null'


@app.route('/computer')
def computer_control():
    global control_method, auto
    return 'computer control'


@app.route('/parameter', methods=['GET', 'POST'])
def parameter():
    global p
    if request.method == 'GET':
        return p.build_to_json()
    else:
        data = request.data
        p.handle_post_parameter(data)
        save_db_parameter(p)
        return 'save success'


def init():
    get_db_parameter(p)
    update_indoor()
    update_outdoor()
    update_control()
    server_connect()
    post_server_data()
    get_web_command()


init()
scheduler1 = Scheduler(60, update_outdoor)
scheduler2 = Scheduler(60, update_indoor)
# scheduler3 = Scheduler(30, update_control)
server_scheduler = Scheduler(60, server_connect)
post_server_scheduler = Scheduler(60, post_server_data)
get_web_command_scheduler = Scheduler(0.5, get_web_command)
scheduler1.start()
scheduler2.start()
# scheduler3.start()
server_scheduler.start()
post_server_scheduler.start()
get_web_command_scheduler.start()

if __name__ == '__main__':
    app.run('0.0.0.0', '8020', threaded=True)
    scheduler1.stop()
    scheduler2.stop()
    server_scheduler.stop()
    get_web_command_scheduler.stop()
    get_web_command_scheduler.stop()
    # scheduler3.stop()
