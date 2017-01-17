# coding=utf-8

import json
import urllib

import requests
from flask import Flask, request

import sensor
from autorun import auto_run_main, get_side_wait_time
from control import Control
from currenttime import get_current_time
from database import save_db_indoor, save_db_outdoor, save_db_control, get_db_parameter, save_db_parameter, \
    get_db_indoor, get_db_outdoor, delete_db_data
from indoor import Indoor
from outdoor import Outdoor
from parameter import Parameter
from scheduler import Scheduler

r = requests
app = Flask(__name__)

# 测试节点数据
node0 = Indoor('1')

# 室外环境数据
outdoor = Outdoor()
c = Control()

# 参数数据
p = Parameter()

control_method = "computer"
isConnect = False

# 服务器url
url = "http://121.43.106.119:8090/"
start_time = get_current_time()
indoor_node_data = ''''''


def server_connect():
    """ 测试与服务器连接状况 """
    global isConnect, start_time
    try:
        data = urllib.urlopen(url).read()
        if data == 'success':
            isConnect = True
        print 'server connect success'
    except:
        start_time = get_current_time()
        isConnect = False
        print 'server disconnect'


def post_server_data():
    """ 把记录在数据库的室内、室外环境数据发送到服务器端，若成功则删除本地数据库内记录 """
    global isConnect
    if isConnect:
        try:
            url_indoor = url + 'indoor'
            post_data = get_db_indoor(start_time)
            # eval(post_data)
            delete_db_data('indoor')
            # post_data=urllib.urlencode(post_data)
            # request = urllib2.Request(url, post_data)
            # response = urllib2.urlopen(request)
            # print response.read()
            r.post(url_indoor, post_data)
        except:
            print 'post indoor data fail, please review'
        try:
            url_outdoor = url + 'outdoor'
            post_data = get_db_outdoor(start_time)
            delete_db_data('outdoor')
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
    """ 从无线传感器获取温室内各个节点测量的环境数据 """
    global start_time, indoor_node_data
    indoor_node_data = sensor.get_sensor_data()
    if isConnect:
        start_time = get_current_time()
    obj = json.loads(indoor_node_data)
    for key in obj.keys():
        node0.set_name(key)
        value = obj.get(key)
        node0.set_update_time(value['update_time'])
        node0.set_co2(value['co2'])
        node0.set_temperature(value['temperature'])
        node0.set_humidity(value['humidity'])
        save_db_indoor(node0)
    print 'indoor updated', get_current_time()


def update_outdoor():
    """ 获取温室外环境数据，从服务器端获得 """
    try:
        outdoor.get_weather_from_api()
        outdoor.set_wind_direction_number()
    except:
        print 'get outdoor from weather api error'
    outdoor.set_update_time(get_current_time())
    save_db_outdoor(outdoor)
    print 'outdoor updated', get_current_time()


def update_control():
    """ 传感器状态更新 """
    # save_db_control(c)
    print 'control updated', get_current_time()


def auto_running():
    """ 温室自控算法 """
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
    """ 处理服务器及其他设备对被控对象（继电器）的手动控制请求 """
    global r
    if request.method == 'POST':
        try:
            data = request.data
            c.set_update_time(get_current_time())
            r = c.handle_post(data)
            save_db_control(c)
            return r
        except:
            return "post error"
    else:
        return c.build_json()


@app.route('/auto', methods=['GET', 'POST'])
def auto_run():
    """ 处理请求：启动、关闭自动控制算法控制温室 """
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


@app.route('/stationState')
def stationState():
    global isConnect
    if request.method == 'GET':
        if isConnect:
            return '''系统正常运行'''
        else:
            return '''基站运行正常，服务器连接失败，请检查网络'''


@app.route('/computer')
def computer_control():
    global control_method, auto
    return 'computer control'


@app.route('/parameter', methods=['GET', 'POST'])
def parameter():
    """ 处理服务器及其他设备对参数读取、修改的请求 """
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
scheduler1 = Scheduler(300, update_outdoor)
scheduler2 = Scheduler(300, update_indoor)
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
    post_server_scheduler.stop()
    # scheduler3.stop()
