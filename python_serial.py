#!/usr/bin/python
# coding=UTF-8

import serial

###################################################
#
# 功 能: 将接收到的数据已hex显示
# 参 数: 串口接受到的数据
# 返 回: 转换后的数据
#
###################################################

def hexshow(data):
    hex_data = ''
    hLen = len(data)
    for i in xrange(hLen):
        hvol = ord(data[i])
        hhex = '%02x' % hvol
        hex_data += hhex+' '
    print('hexshow:', hex_data)


###################################################
#
# 功 能: 将需要发送的字符串以hex形式发送
# 参 数: 待发送的数据
# 返 回: 转换后的数据
#
###################################################

def hexsend(string_data=''):
    hex_data = string_data.decode("hex")
    return hex_data



if __name__ == '__main__':
    # ~ serial = serial.Serial('/dev/ttyS0', 115200)
    serial = serial.Serial('COM9', 57600)# 打开COM1并设置波特率为115200，COM1只适用于Windows
    print( serial)
    if serial.isOpen():
       print("open success")
    else:
        print("open failed")


    try:
        while True:
            count = serial.inWaiting()
            if count > 0:
                data = serial.read(count)
                if data != b'':
                    print("receive:", data)
                    serial.write(data)
                else:
                    serial.write(hexsend(data))
    except KeyboardInterrupt:
        if serial != None:
            serial.close()
