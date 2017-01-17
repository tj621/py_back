# coding=utf-8
'''

@author: Zxh
'''


def relay_number(number):
    relay_1st_on = "0%s 05 00 00 FF 00 8C 3A" % (number)
    relay_1st_off = "0%s 05 00 00 00 00 CD CA" % (number)
    relay_2nd_on = "0%s 05 00 01 FF 00 DD FA" % (number)
    relay_2nd_off = "0%s 05 00 01 00 00 9C 0A" % (number)
    relay_3rd_on = "0%s 05 00 02 FF 00 2D FA" % (number)
    relay_3rd_off = "0%s 05 00 02 00 00 6C 0A" % (number)
    relay_4th_on = "0%s 05 00 03 FF 00 7C 3A" % (number)
    relay_4th_off = "0%s 05 00 03 00 00 3D CA" % (number)
    relay_5th_on = "0%s 05 00 04 FF 00 CD FB" % (number)
    relay_5th_off = "0%s 05 00 04 00 00 8C 0B" % (number)
    relay_6th_on = "0%s 05 00 05 FF 00 9C 3B" % (number)
    relay_6th_off = "0%s 05 00 05 00 00 DD CB" % (number)
    relay_7th_on = "0%s 05 00 06 FF 00 6C 3B" % (number)
    relay_7th_off = "0%s 05 00 06 00 00 2D CB " % (number)
    relay_8th_on = "0%s 05 00 07 FF 00 3D FB" % (number)
    relay_8th_off = "0%s 05 00 07 00 00 7C 0B" % (number)
    if number == 1:
        str = 'first'
    elif number == 2:
        str = 'second'
    elif number == 3:
        str = 'third'
    elif number == 4:
        str = 'forth'
    relay = str + '_1st'
    first_1st = (relay_1st_on, relay_1st_off)
    first_2nd = (relay_2nd_on, relay_2nd_off)
    first_3rd = (relay_3rd_on, relay_3rd_off)
    first_4th = (relay_4th_on, relay_4th_off)
    first_5th = (relay_5th_on, relay_5th_off)
    first_6th = (relay_6th_on, relay_6th_off)
    first_7th = (relay_7th_on, relay_7th_off)
    first_8th = (relay_8th_on, relay_8th_off)
    first_relay = [first_1st, first_2nd, first_3rd, first_4th, first_5th, first_6th, first_7th, first_8th]
