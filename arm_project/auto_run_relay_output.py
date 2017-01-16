# coding=utf-8

'''

@author: Zxh
'''
from time import sleep
from relay_output import tri_state_relay_output
import urllib2
import urllib

roof_state = {"open all to close": -1,
              "open half to close": -0.7,
              "open small to close": -0.5,
              "close to open all": 1,
              "open small to open all": 2,
              "open half to open all": 2,
              "close to open small": 0.1,
              "open half to open small": 1.1,
              "open all to open small": 1.1,
              "close to open half": 0.5,
              "open small to open half": 1.5,
              "open all to open half": 1.5,
              "": 0
}
screen_state = {"open to close": -1,
                "": 0,
                "close to open": 1}

side_state = {"open to close": -1,
              "close to open all": 1,
              "close to open half": 0.5,
              "open all to open half": 1.5,
              "open half to open all": 2,
              "": 0
}


def roof_run_and_stop(time, key):
    value = roof_state.get(key)
    if value < 0:
        # data={"roof_vent_south": "off"}
        tri_state_relay_output("roof_vent_south", "off")
        #post_localhost_control(data)
        #data={"roof_vent_north": "off"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_north", "off")
        sleep(time)
        #data={"roof_vent_south": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_south", "stop")
        #data={"roof_vent_north": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_north", "stop")
    elif value > 1:
        # data={"roof_vent_south": "off"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_south", "off")
        #data={"roof_vent_north": "off"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_north", "off")
        sleep(time)
        #data={"roof_vent_south": "on"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_south", "on")
        #data={"roof_vent_north": "on"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_north", "on")
        sleep(time * (value - 1))
        #data={"roof_vent_south": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_south", "stop")
        #data={"roof_vent_north": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_north", "stop")
    elif value != 0:
        # data={"roof_vent_south": "on"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_south", "on")
        #data={"roof_vent_north": "on"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_north", "on")
        sleep(time * value)
        #data={"roof_vent_south": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_south", "stop")
        #data={"roof_vent_north": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("roof_vent_north", "stop")
    else:
        print 'the state is same as before'


def side_vent_run_and_stop(time, key):
    value = side_state.get(key)
    if value < 0:
        # data={"side_vent": "off"}
        #post_localhost_control(data)
        tri_state_relay_output("side_vent", "off")
        sleep(time)
        #data={"side_vent": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("side_vent", "stop")
    elif value > 1:
        # data={"side_vent": "off"}
        #post_localhost_control(data)
        tri_state_relay_output("side_vent", "off")
        sleep(time)
        #data={"side_vent": "on"}
        #post_localhost_control(data)
        tri_state_relay_output("side_vent", "on")
        sleep(time * (value - 1))
        #data={"side_vent": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("side_vent", "stop")
    elif value != 0:
        # data={"side_vent": "on"}
        #post_localhost_control(data)
        tri_state_relay_output("side_vent", "on")
        sleep(time * value)
        #data={"side_vent": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("side_vent", "stop")
    else:
        print 'the state is same as before'


def shade_screen_out_run_and_stop(time, key):
    # print 'shade screen out thread start'
    value = screen_state.get(key)
    if value < 0:
        #data={"shade_screen_out": "off"}
        #post_localhost_control(data)
        tri_state_relay_output("shade_screen_out", "off")
        sleep(time)
        #data={"shade_screen_out": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("shade_screen_out", "stop")
    elif value != 0:
        #data={"shade_screen_out": "on"}
        #post_localhost_control(data)
        tri_state_relay_output("shade_screen_out", "on")
        sleep(time)
        #data={"shade_screen_out": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("shade_screen_out", "stop")
    else:
        print 'the state is same as before'


def shade_screen_in_run_and_stop(time, key):
    # print 'shade screen in thread start'
    value = screen_state.get(key)
    if value < 0:
        #data={"shade_screen_in": "off"}
        #post_localhost_control(data)
        tri_state_relay_output("shade_screen_in", "off")
        sleep(time)
        #data={"shade_screen_in": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("shade_screen_in", "stop")
    elif value != 0:
        #data={"shade_screen_in": "on"}
        #post_localhost_control(data)
        tri_state_relay_output("shade_screen_in", "on")
        sleep(time)
        #data={"shade_screen_in": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("shade_screen_in", "stop")
    else:
        print 'the state is same as before'


def thermal_screen_run_and_stop(time, key):
    # print 'thermal screen thread start'
    value = screen_state.get(key)
    if value < 0:
        #data={"thermal_screen": "off"}
        #post_localhost_control(data)
        tri_state_relay_output("thermal_screen", "off")
        sleep(time)
        #data={"thermal_screen": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("thermal_screen", "stop")
    elif value != 0:
        #data={"thermal_screen": "on"}
        #post_localhost_control(data)
        tri_state_relay_output("thermal_screen", "on")
        sleep(time)
        #data={"thermal_screen": "stop"}
        #post_localhost_control(data)
        tri_state_relay_output("thermal_screen", "stop")
    else:
        print 'the state is same as before'


def post_localhost_control(value):
    url = 'http://localhost:8020/control'
    post_data = urllib.urlencode(value)
    urllib2.urlopen(url, post_data)
