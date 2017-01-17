# coding=utf-8

import crcmod

# 经过测试 继电器指令符合 modbus
crc16 = crcmod.predefined.mkCrcFun('modbus')

# 几号继电器 1号赋值0x01
th = 0x02

# 指令格式：ID  功能码      接口号 开关	      CRC16_L CRC16_H
frame_ = [0x00, 0x05, 0x00, 0x01, 0xFF, 0x00]

on_off = True
for i in range(16):
    frame = frame_

    frame[0] = th

    frame[3] = i / 2

    on_off = not on_off
    if on_off:
        frame[4] = 0x00
    else:
        frame[4] = 0xFF

    frame_str = [' ' + '{:02X}'.format(n) for n in frame]

    CRC_hex = crc16("".join(['{:02X}'.format(n) for n in frame]).decode("hex"))
    CRC_str = '{:04X}'.format(CRC_hex)

    print "".join(frame_str), CRC_str[2:] + ' ' + CRC_str[:2]
