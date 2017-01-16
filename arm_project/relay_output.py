# coding=utf-8
'''

@author: Zxh
'''
from serial_output import send_command

first_1st_on = "01 05 00 00 FF 00 8C 3A"
first_1st_off = "01 05 00 00 00 00 CD CA"
first_2nd_on = "01 05 00 01 FF 00 DD FA"
first_2nd_off = "01 05 00 01 00 00 9C 0A"
first_3rd_on = "01 05 00 02 FF 00 2D FA"
first_3rd_off = "01 05 00 02 00 00 6C 0A"
first_4th_on = "01 05 00 03 FF 00 7C 3A"
first_4th_off = "01 05 00 03 00 00 3D CA"
first_5th_on = "01 05 00 04 FF 00 CD FB"
first_5th_off = "01 05 00 04 00 00 8C 0B"
first_6th_on = "01 05 00 05 FF 00 9C 3B"
first_6th_off = "01 05 00 05 00 00 DD CB"
first_7th_on = "01 05 00 06 FF 00 6C 3B"
first_7th_off = "01 05 00 06 00 00 2D CB "
first_8th_on = "01 05 00 07 FF 00 3D FB"
first_8th_off = "01 05 00 07 00 00 7C 0B"

first_1st = (first_1st_off, first_1st_on)
first_2nd = (first_2nd_off, first_2nd_on )
first_3rd = (first_3rd_off, first_3rd_on)
first_4th = (first_4th_off, first_4th_on)
first_5th = (first_5th_off, first_5th_on)
first_6th = (first_6th_off, first_6th_on)
first_7th = (first_7th_off, first_7th_on)
first_8th = (first_8th_off, first_8th_on)
first_open_all = "01 0F 00 00 00 08 01 FF BE D5"
first_close_all = "01 0F 00 00 00 08 01 00 FE 95"
first_query_all = "01 01 00 00 00 08 3D CC"
first_relay = [first_1st, first_2nd, first_3rd, first_4th, first_5th, first_6th, first_7th, first_8th]

second_1st_on = "02 05 00 00 FF 00 8C 09"
second_1st_off = "02 05 00 00 00 00 CD F9"
second_2nd_on = "02 05 00 01 FF 00 DD C9"
second_2nd_off = "02 05 00 01 00 00 9C 39"
second_3rd_on = "02 05 00 02 FF 00 2D C9"
second_3rd_off = "02 05 00 02 00 00 6C 39"
second_4th_on = "02 05 00 03 FF 00 7C 09"
second_4th_off = "02 05 00 03 00 00 3D F9"
second_5th_on = "02 05 00 04 FF 00 CD C8"
second_5th_off = "02 05 00 04 00 00 8C 38"
second_6th_on = "02 05 00 05 FF 00 9C 08"
second_6th_off = "02 05 00 05 00 00 DD F8"
second_7th_on = "02 05 00 06 FF 00 6C 08"
second_7th_off = "02 05 00 06 00 00 2D F8 "
second_8th_on = "02 05 00 07 FF 00 3D C8"
second_8th_off = "02 05 00 07 00 00 7C 38"

second_1st = (second_1st_off, second_1st_on)
second_2nd = (second_2nd_off, second_2nd_on )
second_3rd = (second_3rd_off, second_3rd_on)
second_4th = (second_4th_off, second_4th_on)
second_5th = (second_5th_off, second_5th_on)
second_6th = (second_6th_off, second_6th_on)
second_7th = (second_7th_off, second_7th_on)
second_8th = (second_8th_off, second_8th_on)
second_open_all = "02 0F 00 00 00 08 01 FF FE C0"
second_close_all = "02 0F 00 00 00 08 01 00 BE 80"
second_query_all = "02 01 00 00 00 08 3D FF"
second_relay = [second_1st, second_2nd, second_3rd, second_4th, second_5th, second_6th, second_7th, second_8th]

third_1st_on = "03 05 00 00 FF 00 8D D8"
third_1st_off = "03 05 00 00 00 00 CC 28"
third_2nd_on = "03 05 00 01 FF 00 DC 18"
third_2nd_off = "03 05 00 01 00 00 9D E8"
third_3rd_on = "03 05 00 02 FF 00 2C 18"
third_3rd_off = "03 05 00 02 00 00 6D E8"
third_4th_on = "03 05 00 03 FF 00 7D D8"
third_4th_off = "03 05 00 03 00 00 3C 28"
third_5th_on = "03 05 00 04 FF 00 CC 19"
third_5th_off = "03 05 00 04 00 00 8D E9"
third_6th_on = "03 05 00 05 FF 00 9D D9"
third_6th_off = "03 05 00 05 00 00 DC 29"
third_7th_on = "03 05 00 06 FF 00 6D D9"
third_7th_off = "03 05 00 06 00 00 2C 29 "
third_8th_on = "03 05 00 07 FF 00 3C 19"
third_8th_off = "03 05 00 07 00 00 7D E9"

third_1st = (third_1st_off, third_1st_on)
third_2nd = (third_2nd_off, third_2nd_on )
third_3rd = (third_3rd_off, third_3rd_on)
third_4th = (third_4th_off, third_4th_on)
third_5th = (third_5th_off, third_5th_on)
third_6th = (third_6th_off, third_6th_on)
third_7th = (third_7th_off, third_7th_on)
third_8th = (third_8th_off, third_8th_on)
third_open_all = "03 0F 00 00 00 08 01 FF 3F 0C"
third_close_all = "03 0F 00 00 00 08 01 00 7F 4C"
third_query_all = "03 01 00 00 00 08 3C 2E"
third_relay = [third_1st, third_2nd, third_3rd, third_4th, third_5th, third_6th, third_7th, third_8th]

# post={"roof_vent_south":"on"}
control_relay = {
    "tri_state": {
        "roof_vent_south": {
            "on": first_relay[0],
            "off": first_relay[1]
        },
        "roof_vent_north": {
            "on": first_relay[2],
            "off": first_relay[3]
        },
        "side_vent": {
            "on": first_relay[4],
            "off": first_relay[5]
        },
        "shade_screen_north": {
            "on": first_relay[6],
            "off": first_relay[7]
        },
        "shade_screen_south": {
            "on": second_relay[0],
            "off": second_relay[1]
        },
        "thermal_screen": {
            "on": second_relay[2],
            "off": second_relay[3]
        }
    },
    "bi_state": {
        "cooling_pump": second_relay[4],
        "fogging": second_relay[5],
        "heating": second_relay[6],
        "co2": second_relay[7],
        "lighting_1": third_relay[0],
        "lighting_2": third_relay[1],
        "irrigation": third_relay[2]
    }
}


def bi_state_relay_output(key, value):
    relay = control_relay.get("bi_state")
    str1 = relay.get(key)
    if value == "on":
        out_str = str1[1]
    else:
        out_str = str1[0]
    send_command(out_str)
    print '%s relay off ' % key



def tri_state_relay_output(key, value):
    relay = control_relay.get("tri_state")
    str1 = relay.get(key)
    if value == "on":
        out_str = str1.get("on")[1]
        send_command(out_str)
        print '%s relay01 on ' % key
        out_str = str1.get("off")[0]
        send_command(out_str)
        print '%s relay02 off ' % key
    elif value == "off":
        out_str = str1.get("on")[0]
        send_command(out_str)
        print '%s relay01 off ' % key
        out_str = str1.get("off")[1]
        send_command(out_str)
        print '%s relay02 on ' % key
    else:
        out_str = str1.get("off")[0]
        send_command(out_str)
        print '%s relay01 off ' % key
        out_str = str1.get("on")[0]
        send_command(out_str)
        print '%s relay02 off ' % key
    print key + ': ' + value

#
# str="lighting_2"
# print control_relay.get("bi_state").get(str)
# print "%s relay01 off" %str
# test_first=[first_1st_on,first_1st_off,first_2nd_on,first_2nd_off,first_3rd_on,first_3rd_off,first_4th_on,first_4th_off,first_5th_on,first_5th_off,first_6th_on,first_6th_off
# ,first_7th_on,first_7th_off,first_8th_on,first_8th_off,first_open_all,first_close_all]
# for test in test_first:
#     send_command(test)
#
# test_third=[third_1st_on,third_1st_off,third_2nd_on,third_2nd_off,third_3rd_on,third_3rd_off,third_4th_on,third_4th_off,third_5th_on,third_5th_off,third_6th_on,third_6th_off
#     ,third_7th_on,third_7th_off,third_8th_on,third_8th_off,third_open_all,third_close_all]
# for test in test_third:
#     send_command(test)
