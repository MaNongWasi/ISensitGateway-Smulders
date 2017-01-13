import serial
import struct
import time
import threading
import datetime
import math

import sys
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)
from isensit_sql import *


def printResult(result):
    if len(result) > 0:
	for i in result:
            print struct.unpack('<B', i)

def pick_data(result, startP, endP):
    format = '<' + str(endP - startP) + 'B'
    return struct.unpack(format, result[startP:endP])

def parse_data(data):
    result = [data[2], data[3], data[0], data[1]]
    b = struct.pack('4B', *result)
    f = struct.unpack('>f', b)
    return f[0] 

def findData(result):
    i = 0
    while len(result) > (20 - i) and pick_data(result, i-21, i-18) != (5, 4, 16):
        i = i - 1
    if len(result) > (20 - i):
	if len(result) == 21:
            return result[i-21:]
	else:
            return result[i-21: i]
    else:
	return False

def get_data():
    global r
    registers = findData(r)
#    printResult(registers)
    if registers is not False:
 	printResult(registers)
        pm = parse_data(pick_data(registers, 3, 7))
        temp = parse_data(pick_data(registers, 7,11))
        hum = parse_data(pick_data(registers, 11,15))
        pm_hour = parse_data(pick_data(registers, 15, 19))

 	print datetime.datetime.now()
        print "PM= %.1f" % pm
        print "TEMP: %.2f" % temp
        print "HUM: %.2f" % hum
        print "PM HOUR: %.1f" % pm_hour
	print "-----------------------------"
	if math.fabs(pm) < 10000 and math.fabs(temp) < 10000 and math.fabs(hum) < 10000:
	    db.connect_to_db()
            db.insert_fd_data(fd_id, pm, temp, hum, pm_hour, db.get_shift())
	    db.close_db()
    r = ""
    global running
    if running:
        t = threading.Timer(sleeptime, get_data)
        t.start()
	running = False
    else:
        print "System exit"
        exit = True
	exit(-1)

r = ""
running = True
exit = False

try:
    # initialize database reader
    db = ISensitGWMysql()
    sleeptime = db.sleeptime
    fd_id = db.config_data.get_fd_id()
#    db.connect_to_db()
except Exception as e:
    print("Error in initializing db, reason: ", str(e))
    running = False
    exit(-1)


ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS,
    timeout = 1.0
)  

#print(ser.isOpen())

t = threading.Timer(sleeptime, get_data)
t.start()

#while 1:
while not exit:
    running = True
    ser.write("\x05\x04\x00\x02\x00\x08\x51\x88")
    recv = ser.read(21)
    r = r + recv
#    print len(r)
    time.sleep(2.0)
#    print "+++++++++++++++++++++++++++++++++++++"

ser.close()
#db.close_db()
