# coding=utf-8

'''

@author: Zxh
'''
from currenttime import get_current_hour, get_current_month, get_time

from relay_output import bi_state_relay_output
import threading
from auto_run_relay_output import shade_screen_out_run_and_stop, \
    roof_run_and_stop, side_vent_run_and_stop
from time import sleep
from control import Control
from database import save_db_control

temp = Control()

temperature_set_temp0 = 1
temperature_set_temp1 = 1
temperature_set_temp2 = 1
side_wait_time = 1

lighting_open_time = 0
lighting_open_time2 = 0
lighting_stop_time = 0
lighting_stop_time2 = 0
lighting_stop_time3 = 0

roof_state = ""
shade_screen_out_state = ""
shade_screen_in_state = ""
side_vent_state = ""
thermal_screen_state = ""

shade_screen_out_time = 1
roof_open_time = 1
side_open_time = 1
thermal_time = 1
shade_screen_in_time = 1

auto_lighting_1 = ''
auto_lighting_2 = ''

angle = "zero"
bad_weather = "false"


def init_pram():
    global shade_screen_out_time, roof_open_time, side_open_time, thermal_time, shade_screen_in_time, thermal_screen_state
    global temperature_set_temp0, temperature_set_temp1, temperature_set_temp2, side_wait_time, lighting_open_time, lighting_open_time2
    global lighting_stop_time, lighting_stop_time2, lighting_stop_time3, roof_state, shade_screen_out_state, side_vent_state, shade_screen_in_state
    global angle, bad_weather
    temperature_set_temp0 = 1
    temperature_set_temp1 = 1
    temperature_set_temp2 = 1
    side_wait_time = 1

    lighting_open_time = 0
    lighting_open_time2 = 0
    lighting_stop_time = 0
    lighting_stop_time2 = 0
    lighting_stop_time3 = 0

    roof_state = "open all to close"
    shade_screen_out_state = "open to close"
    shade_screen_in_state = "open to close"
    side_vent_state = "open to close"
    thermal_screen_state = "open to close"

    shade_screen_out_time = 1
    roof_open_time = 1
    side_open_time = 1
    thermal_time = 1
    shade_screen_in_time = 1

    angle = "zero"
    bad_weather = "false"


def auto_run_main(Indoor, Outdoor, Control, Parameter):
    global shade_screen_out_time, roof_open_time, side_open_time, thermal_time, shade_screen_in_time
    get_current_control_state(Indoor, Control, Parameter)
    co2_control(Indoor, Parameter)
    shade_screen_out_control(Outdoor, Parameter)
    cooling_pad_control(Indoor, Parameter)
    fogging_control(Indoor, Parameter)
    roof_vent_control(Outdoor, Parameter, Indoor)
    side_vent_control(Indoor, Parameter)
    thermal_screen_control(Outdoor, Parameter)
    heating_control(Indoor, Parameter)
    shade_screen_in_control(Outdoor, Parameter)
    lighting_control(Outdoor, Parameter)

    get_current_state_to_save()

    maxtime = max(shade_screen_out_time, roof_open_time * 2, side_open_time * 1.5, thermal_time, shade_screen_in_time)
    threads = []
    t1 = threading.Thread(target=shade_screen_in_thread)
    t2 = threading.Thread(target=roof_vent_thread)
    t3 = threading.Thread(target=side_vent_thread)
    t4 = threading.Thread(target=thermal_screen_thread)
    t5 = threading.Thread(target=shade_screen_out_thread)
    threads.append(t1)
    threads.append(t2)
    threads.append(t3)
    threads.append(t4)
    threads.append(t5)
    for t in threads:
        # t.setDaemon(False)
        t.start()
    sleep(maxtime)
    sleep(2)
    print 'game over'


def shade_screen_out_thread():
    global shade_screen_out_state, shade_screen_out_time
    shade_screen_out_run_and_stop(shade_screen_out_time, shade_screen_out_state)


def roof_vent_thread():
    global roof_open_time, roof_state
    roof_run_and_stop(roof_open_time, roof_state)


def side_vent_thread():
    global side_open_time, side_vent_state
    side_vent_run_and_stop(side_open_time, side_vent_state)


def thermal_screen_thread():
    global thermal_time, thermal_screen_state
    roof_run_and_stop(thermal_time, thermal_screen_state)


def shade_screen_in_thread():
    global shade_screen_in_time, shade_screen_in_state
    roof_run_and_stop(shade_screen_in_time, shade_screen_in_state)


def get_side_wait_time():
    global auto_indoor_temperature, temperature_set_temp2, side_open_time, side_wait_time
    if auto_indoor_temperature > (temperature_set_temp2 + side_open_time):
        if side_wait_time < side_open_time:
            side_wait_time += 1
            print side_wait_time


def get_current_control_state(Indoor, Control, Parameter):
    global auto_roof_vent_south, auto_roof_vent_north, auto_side_vent, auto_shade_screen_out, auto_shade_screen_in, auto_thermal_screen, auto_cooling_pad, auto_fogging, auto_heating, auto_co2
    global auto_lighting_1, auto_lighting_2, auto_irrigation, shade_screen_out_time, roof_open_time, side_open_time, thermal_time, shade_screen_in_time
    global auto_indoor_temperature
    auto_cooling_pad = Control.get_cooling_fan()
    auto_roof_vent_south = Control.get_roof_vent_south()
    auto_roof_vent_north = Control.get_roof_vent_north()
    auto_side_vent = Control.get_side_vent()
    auto_shade_screen_out = Control.get_shade_screen_north()
    auto_shade_screen_in = Control.get_shade_screen_south()
    auto_thermal_screen = Control.get_thermal_screen()
    auto_fogging = Control.get_fogging()
    auto_heating = Control.get_heating()
    auto_co2 = Control.get_co2()
    auto_lighting_1 = Control.get_lighting_1()
    auto_lighting_2 = Control.get_lighting_2()
    auto_irrigation = Control.get_irrigation()

    shade_screen_out_time = int(Parameter.get_shade_screen_out_open_time())
    roof_open_time = int(Parameter.get_roof_vent_open_time())
    side_open_time = int(Parameter.get_side_vent_open_time())
    thermal_time = int(Parameter.get_thermal_screen_open_time())
    shade_screen_in_time = int(Parameter.get_shade_screen_in_open_time())

    auto_indoor_temperature = Indoor.get_temperature()


def co2_control(Indoor, Parameter):
    global auto_co2
    if Indoor.get_co2() < Parameter.get_co_2_lower_limit():
        bi_state_relay_output("co2", "on")
        auto_co2 = "on"
    elif Indoor.get_co2() > Parameter.get_co_2_upper_limit():
        bi_state_relay_output("co2", "off")
        auto_co2 = "off"


def shade_screen_out_control(Outdoor, Parameter):
    global auto_shade_screen_out, shade_screen_out_state
    if bad_weather == "true":
        if auto_shade_screen_out == "on":
            shade_screen_out_state = "open to close"
        auto_shade_screen_out = "off"
    # self.control.set_shade_screen_out("off")
    elif Outdoor.get_radiation() > Parameter.get_upper_limit_light_to_open_out_shade_screen():
        if auto_shade_screen_out == "off":
            shade_screen_out_state = "close to open"
        auto_shade_screen_out = "on"
    else:
        if auto_shade_screen_out == "on":
            shade_screen_out_state = "open to close"
        auto_shade_screen_out = "off"
    return shade_screen_out_state


def cooling_pad_control(Indoor, Parameter):
    global auto_cooling_pad
    if float(Indoor.get_temperature()) > float(Parameter.get_temperature_to_open_cooling_pad()) + 1:
        bi_state_relay_output("cooling_pad", "on")
        auto_cooling_pad = "on"
    # self.control.set_cooling_pad("on")
    elif float(Indoor.get_temperature()) < float(Parameter.get_temperature_to_open_cooling_pad()) - 1:
        bi_state_relay_output("cooling_pad", "off")
        auto_cooling_pad = "off"


# self.control.set_cooling_pad("off")

def fogging_control(Indoor, Parameter):
    if float(Indoor.get_temperature()) > float(Parameter.get_temperature_to_open_fogging()) + 1:
        bi_state_relay_output("fogging", "on")
        auto_fogging = "on"
    elif float(Indoor.get_temperature()) < float(Parameter.get_temperature_to_open_fogging()) - 1:
        bi_state_relay_output("fogging", "off")
        auto_fogging = "off"


def roof_vent_control(Outdoor, Parameter, Indoor):
    global temperature_set_temp0, temperature_set_temp1, temperature_set_temp2, angle, auto_roof_vent_north, auto_roof_vent_south, roof_start_time, roof_state
    current_hour = get_current_hour()
    roof_start_time = get_time()
    if bad_weather == "true":
        if auto_roof_vent_north == "on" and auto_roof_vent_south == "on":
            roof_state = "open all to close"
            if angle == "half":
                roof_state = "open half to close"
            elif angle == "small":
                roof_state = "open small to close"
        auto_roof_vent_north = "off"
        auto_roof_vent_south = "off"
        angle = "zero"
    else:
        if current_hour >= Parameter.get_time_1() and current_hour < Parameter.get_time_2():
            temperature_set_temp0 = float(Parameter.get_temperature_1())
        elif current_hour >= Parameter.get_time_2() and current_hour < Parameter.get_time_3():
            temperature_set_temp0 = float(Parameter.get_temperature_2())
        elif current_hour >= Parameter.get_time_3() and current_hour < Parameter.get_time_4():
            temperature_set_temp0 = float(Parameter.get_temperature_3())
        else:
            temperature_set_temp0 = float(Parameter.get_temperature_4())

            # humidity influence on temperature
        if float(Parameter.get_humidity_influence_range_of_air_temperature()) == 0:
            print "humidity_influence_range_of_air_temperature can not be 0"
        elif float(Parameter.get_expect_humidity()) == 95:
            print "expect_humidity can not be 95%"
        else:
            if float(Outdoor.get_humidity()) <= (float(Parameter.get_expect_humidity()) - 5 - float(
                    Parameter.get_humidity_influence_range_of_air_temperature())):
                temperature_set_temp1 = temperature_set_temp0 + float(
                    Parameter.get_low_humidity_influence_on_air_temperature())
            elif float(Outdoor.get_humidity()) <= (float(Parameter.get_expect_humidity()) - 5):
                tmpt = (float(Parameter.get_expect_humidity()) - 5 - float(Outdoor.get_humidity())) * float(
                    Parameter.get_low_humidity_influence_on_air_temperature()) / float(
                    Parameter.get_humidity_influence_range_of_air_temperature())
                temperature_set_temp1 = temperature_set_temp0 + tmpt
            elif float(Outdoor.get_humidity()) >= (float(Parameter.get_expect_humidity()) + 5):
                tmpt = (float(Outdoor.get_humidity()) - float(Parameter.get_expect_humidity()) - 5) * float(
                    Parameter.get_high_humidity_influence_on_air_temperature()) / (
                           100 - 5 - float(Parameter.get_expect_humidity()))
                temperature_set_temp1 = temperature_set_temp0 + tmpt
            else:
                temperature_set_temp1 = temperature_set_temp0

        # light influence on temperature
        if Outdoor.get_radiation() < Parameter.get_expect_light():
            temperature_set_temp2 = temperature_set_temp1
        else:
            temperature_set_temp2 = temperature_set_temp1 - float(
                Parameter.get_light_influence_on_air_temperature_slope()) * (float(Outdoor.get_radiation()) - float(
                Parameter.get_expect_light()))
        if temperature_set_temp2 > (temperature_set_temp1 + float(Parameter.get_low_light_influence_on_temperature())):
            temperature_set_temp2 = temperature_set_temp1 + float(Parameter.get_low_light_influence_on_temperature())
        elif temperature_set_temp2 < (
                    temperature_set_temp1 - float(Parameter.get_high_light_influence_on_temperature())):
            temperature_set_temp2 = temperature_set_temp1 - float(Parameter.get_high_light_influence_on_temperature())
        else:
            if temperature_set_temp2 == 0:
                temperature_set_temp2 = 0

        if Outdoor.get_temperature() <= Parameter.get_frost_temperature():
            if auto_roof_vent_north == "on" and auto_roof_vent_south == "on":
                roof_state = "open all to close"
                if angle == "half":
                    roof_state = "open half to close"
                else:
                    roof_state = "open small to close"
            auto_roof_vent_north = "off"
            auto_roof_vent_south = "off"
            angle = "zero"
        elif Outdoor.get_temperature() <= Parameter.get_indoor_temperature_lower_limit():
            # small angle
            if auto_roof_vent_north == "off" and auto_roof_vent_south == "off":
                roof_state = "close to open small"
                if angle == "all":
                    roof_state = "open all to open small"
                elif angle == "half":
                    roof_state = "open half to open small"
            auto_roof_vent_north = "on"
            auto_roof_vent_south = "on"
            angle = "small"
        elif Outdoor.get_temperature() <= temperature_set_temp2:
            # open half
            if auto_roof_vent_north == "off" and auto_roof_vent_south == "off":
                roof_state = "close to open half"
                if angle == "small":
                    roof_state = "open small to half"
                elif angle == "all":
                    roof_state = "open all to open half"
            roof_start_time = get_time()
            auto_roof_vent_north = "on"
            auto_roof_vent_south = "on"
            angle = "half"
        else:
            #
            if auto_roof_vent_north == "off" and auto_roof_vent_south == "off":
                roof_state = "close to open all"
                if angle == "small":
                    roof_state = "open half to all"
                elif angle == "half":
                    roof_state = "open half to open all"
            auto_roof_vent_north = "on"
            auto_roof_vent_south = "on"
            angle = "all"
    return roof_state


def side_vent_control(Indoor, Parameter):
    global auto_side_vent, side_wait_time, side_vent_state, side_angle
    if bad_weather == "true":
        if auto_side_vent == "on":
            side_vent_state = "open to close"
        auto_side_vent = "off"
        side_angle = "zero"
    elif auto_cooling_pad == "on":
        if auto_side_vent == "off":
            side_vent_state = "close to open all"
        auto_side_vent = "on"
        side_angle = "all"
    elif auto_roof_vent_north == "on" and auto_roof_vent_south == "on":
        if side_wait_time < int(Parameter.get_wait_time_to_open_side()):
            if auto_side_vent == "on":
                side_vent_state = "open to close"
            auto_side_vent = "off"
            side_angle = "zero"
        elif side_wait_time > float(Parameter.get_wait_time_to_open_side()) and side_wait_time < 2 * float(
                Parameter.get_wait_time_to_open_side()):
            # half open
            if auto_side_vent == "off":
                side_vent_state = "close to open half"
            elif side_angle == "all":
                side_vent_state = "open all to open half"
            auto_side_vent = "on"
            side_angle = "half"
        elif side_wait_time > 2 * float(Parameter.get_wait_time_to_open_side()):
            # open all
            if auto_side_vent == "off":
                side_vent_state = "close to open all"
            elif side_angle == "half":
                side_vent_state = "open half to open all"
            auto_side_vent = "on"
            side_angle = "all"
        elif Indoor.get_temperature() < (temperature_set_temp2 + float(Parameter.get_temperature_to_open_side())):
            if auto_side_vent == "on":
                side_vent_state = "close to open all"
            auto_side_vent = "off"
            side_wait_time = 0
            side_angle = "zero"
    return side_vent_state


def thermal_screen_control(Outdoor, Parameter):
    global auto_thermal_screen, thermal_screen_state
    if bad_weather == "true":
        if auto_thermal_screen == "on":
            thermal_screen_state = "open to close"
        auto_thermal_screen = "off"
    elif auto_fogging == "on":
        if auto_thermal_screen == "on":
            thermal_screen_state = "open to close"
        auto_thermal_screen = "off"
    else:
        current_hour = get_current_hour()
        current_month = get_current_month()
        if current_month > Parameter.get_month_to_open_thermal_screen() and current_month < Parameter.get_month_to_close_thermal_screen():
            if current_hour > Parameter.get_time_to_open_thermal_screen() and current_hour < Parameter.get_time_to_close_thermal_screen():
                if auto_thermal_screen == "off":
                    thermal_screen_state = "close to open"
                auto_thermal_screen = "on"
            if auto_thermal_screen == "on":
                thermal_screen_state = "open to close"
        auto_thermal_screen = "off"
    return thermal_screen_state


def heating_control(Indoor, Parameter):  # ok
    if Indoor.get_temperature() < Parameter.get_heating_start_lowest_temperature():
        bi_state_relay_output("heating", "on")
        auto_heating = "on"
    elif Indoor.get_temperature() > Parameter.get_heating_stop_highest_temperature():
        bi_state_relay_output("heating", "on")
        auto_heating = "off"


def shade_screen_in_control(Outdoor, Parameter):
    global auto_shade_screen_in, shade_screen_in_state
    if auto_thermal_screen == "on":
        if auto_shade_screen_in == "off":
            shade_screen_in_state = "close to open"
        auto_shade_screen_in = "on"
    elif Outdoor.get_radiation() > Parameter.get_upper_limit_light_to_open_in_shade_screen():
        if auto_shade_screen_in == "on":
            shade_screen_in_state = "open to close"
        auto_shade_screen_in = "off"
    else:
        if auto_shade_screen_in == "off":
            shade_screen_in_state = "close to open"
        auto_shade_screen_in = "on"
    return shade_screen_in_state


def lighting_control(Outdoor, Parameter):
    global t1, t2, t3, t4, t5, lighting_stop_time, lighting_stop_time2, lighting_stop_time3, lighting_open_time, lighting_open_time2
    global auto_lighting_1, auto_lighting_2
    month = int(get_current_month())
    hour = int(get_current_hour())

    if auto_lighting_1 == "off" and auto_lighting_2 == "off":
        if month > Parameter.get_month_to_open_lighting() and month < Parameter.get_month_to_close_lighting():
            if hour > Parameter.get_period_1_start_lighting() and hour < Parameter.get_period_1_stop_lighting():
                if Outdoor.get_radiation() < Parameter.get_radiation_1_to_open_lighting():
                    bi_state_relay_output("lighting_1", "on")
                    auto_lighting_1 = "on"
                    lighting_open_time = get_time()
            elif hour > Parameter.get_period_2_start_lighting() and hour < Parameter.get_period_2_stop_lighting():
                if Outdoor.get_radiation() < Parameter.get_radiation_2_to_open_lighting():
                    bi_state_relay_output("lighting_2", "on")
                    auto_lighting_2 = "on"
                    lighting_open_time2 = get_time()

    elif auto_lighting_1 == "on" and auto_lighting_2 == "off":
        t1 = float(get_time() - lighting_open_time)
        t2 = float(get_time() - lighting_open_time2)
        if t1 > 30 and t1 < 60:
            bi_state_relay_output("lighting_2", "on")
            auto_lighting_2 = "on"
        if t2 > 30 and t2 < 60:
            bi_state_relay_output("lighting_2", "on")
            auto_lighting_2 = "on"
    elif auto_lighting_1 == "on" and auto_lighting_2 == "on":
        if hour > Parameter.get_period_1_start_lighting() and hour < Parameter.get_period_1_stop_lighting():
            if Outdoor.get_radiation() > Parameter.get_radiation_1_to_open_lighting():
                bi_state_relay_output("lighting_1", "off")
                auto_lighting_1 = "off"
                lighting_stop_time = get_time()
        elif hour > Parameter.get_period_2_start_lighting() and hour < Parameter.get_period_2_stop_lighting():
            if Outdoor.get_radiation() > Parameter.get_radiation_2_to_open_lighting():
                bi_state_relay_output("lighting_1", "off")
                auto_lighting_1 = "off"
                lighting_stop_time2 = get_time()
        else:
            bi_state_relay_output("lighting_1", "off")
            auto_lighting_1 = "off"
            lighting_stop_time3 = get_time()

    elif auto_lighting_1 == "off" and auto_lighting_2 == "on":
        t3 = get_time() - lighting_stop_time3
        t4 = get_time() - lighting_stop_time2
        t5 = get_time() - lighting_stop_time
        if t3 > 30 and t3 < 60:
            bi_state_relay_output("lighting_2", "off")
            auto_lighting_2 = "off"
        if t4 > 30 and t4 < 60:
            bi_state_relay_output("lighting_2", "off")
            auto_lighting_2 = "off"
        if t5 > 30 and t5 < 60:
            bi_state_relay_output("lighting_2", "off")
            auto_lighting_2 = "off"


def get_current_state_to_save():
    global temp
    global auto_roof_vent_south, auto_roof_vent_north, auto_side_vent, auto_shade_screen_out, auto_shade_screen_in, auto_thermal_screen, auto_cooling_pad, auto_fogging, auto_heating, auto_co2
    global auto_lighting_1, auto_lighting_2, auto_irrigation

    temp.set_cooling_fan(auto_cooling_pad)
    temp.set_roof_vent_south(auto_roof_vent_south)
    temp.set_roof_vent_north(auto_roof_vent_north)
    temp.set_side_vent(auto_side_vent)
    temp.set_shade_screen_north(auto_shade_screen_out)
    temp.set_shade_screen_south(auto_shade_screen_in)
    temp.set_thermal_screen(auto_thermal_screen)
    temp.set_fogging(auto_fogging)
    temp.set_heating(auto_heating)
    temp.set_co2(auto_co2)
    temp.set_lighting_1(auto_lighting_1)
    temp.set_lighting_2(auto_lighting_2)
    temp.set_irrigation(auto_irrigation)
    save_db_control(temp)
