# coding=utf-8

'''
2016/06/20
@author: Zxh
'''
from serial_output import query_all_state
# from control import Control

first_query_all = "01 01 00 00 00 08 3D CC"
second_query_all = "02 01 00 00 00 08 3D FF"
third_query_all = "03 01 00 00 00 08 3C 2E"
query_all = [first_query_all, second_query_all, third_query_all]
# co = Control()

def get_current_relay_state(Control):
    current_state = get_all_state()
    for message in current_state:
        if message != '':
            print message
            relay_number = int(message[0:2])
            relay_state = message[6:8]
            relay_bin = string_to_bin(relay_state)
            get_relay_state(relay_number, relay_bin, Control)
        else:
            print 'nothing return'
    print Control.build_json()
    return Control.build_json()


def get_all_state():
    current_state = []
    for query in query_all:
        recv = query_all_state(query)
        current_state.append(recv)
    return current_state


# def delete_blank(str1):
# x = str1.split()
#     return ''.join(x)

def get_relay_state(relay_number, relay_state, Control):
    if relay_number == '1':
        if relay_state[0] == relay_state[1]:
            if relay_state[0] == '0':  # 0 means off
                Control.set_roof_vent_south("stop")
            else:
                print 'roof_vent_south error'
        elif relay_state[0] == '1' and relay_state[1] == '0':
            Control.set_roof_vent_south("on")
        elif relay_state[0] == '0' and relay_state[1] == '1':
            Control.set_roof_vent_south("off")

        if relay_state[2] == relay_state[3]:
            if relay_state[2] == '0':  # 0 means off
                Control.set_roof_vent_north("stop")
            else:
                print 'roof_vent_south error'
        elif relay_state[2] == '1' and relay_state[3] == '0':
            Control.set_roof_vent_north("on")
        elif relay_state[2] == '0' and relay_state[3] == '1':
            Control.set_roof_vent_north("off")

        if relay_state[4] == relay_state[5]:
            if relay_state[4] == '0':  # 0 means off
                Control.set_side_vent("stop")
            else:
                print 'roof_vent_south error'
        elif relay_state[4] == '1' and relay_state[5] == '0':
            Control.set_side_vent("on")
        elif relay_state[4] == '0' and relay_state[5] == '1':
            Control.set_side_vent("off")

        if relay_state[6] == relay_state[7]:
            if relay_state[6] == '0':  # 0 means off
                Control.set_shade_screen_out("stop")
            else:
                print 'roof_vent_south error'
        elif relay_state[6] == '1' and relay_state[7] == '0':
            Control.set_shade_screen_out("on")
        elif relay_state[6] == '0' and relay_state[7] == '1':
            Control.set_shade_screen_out("off")

    elif relay_number == '2':
        if relay_state[0] == relay_state[1]:
            if relay_state[0] == '0':  # 0 means off
                Control.set_shade_screen_in("stop")
            else:
                print 'roof_vent_south error'
        elif relay_state[0] == '1' and relay_state[1] == '0':
            Control.set_shade_screen_in("on")
        elif relay_state[0] == '0' and relay_state[1] == '1':
            Control.set_shade_screen_in("off")

        if relay_state[2] == relay_state[3]:
            if relay_state[2] == '0':  # 0 means off
                Control.set_thermal_screen("stop")
            else:
                print 'roof_vent_south error'
        elif relay_state[2] == '1' and relay_state[3] == '0':
            Control.set_thermal_screen("on")
        elif relay_state[2] == '0' and relay_state[3] == '1':
            Control.set_thermal_screen("off")

        if relay_state[4] == '1':
            Control.set_cooling_pad("on")
        else:
            Control.set_cooling_pad("off")

        if relay_state[5] == '1':
            Control.set_fogging("on")
        else:
            Control.set_fogging("off")

        if relay_state[6] == '1':
            Control.set_heating("on")
        else:
            Control.set_heating("off")

        if relay_state[7] == '1':
            Control.set_co_2("on")
        else:
            Control.set_co_2("off")

    elif relay_number == '3':
        if relay_state[0] == '1':
            Control.set_lighting_1("on")
        else:
            Control.set_lighting_1("off")

        if relay_state[1] == '1':
            Control.set_lighting_2("on")
        else:
            Control.set_lighting_2("off")

        if relay_state[2] == '1':
            Control.set_irrigation("on")
        else:
            Control.set_irrigation("off")
    else:
        print 'relay_nymber error'


def string_to_bin(str_in):
    a = '{0:b}'.format(int(str_in, 16))
    str2 = ''
    if len(str(a)) < 7:
        for i in range(8 - len(str(a))):
            str2 += '0'
    return str2 + str(a)

    # str2="EF"
    # print '{0:b}'.format(int(str2,16))
    # get_control_state(Query_all_return,co)
    # current_state=get_all_state()
    # for message in current_state:
    #     if message !='':
    #         print message
    #         relay_number = int(message[0:2])
    #         relay_state = message[6:8]
    #         relay_bin = string_to_bin(relay_state)
    #         print 'relay_number:',relay_number
    #         print 'relay_state:'+relay_bin
    #     else:
    #         print 'nothing return'