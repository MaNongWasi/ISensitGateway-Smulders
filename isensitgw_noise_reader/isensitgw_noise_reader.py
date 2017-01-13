import sys
import usb.core
import time
import threading
import datetime

api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)
from isensit_sql import *

def read_data():
    ret = dev.ctrl_transfer(0xC0, 4, 0, 0,200)
#    print "ret ", ret
    dB = (ret[0] + ((ret[1] & 3) * 256)) * 0.1 + 30
    return dB

def insert_data():
    global data
    currenttime = datetime.datetime.now()
    print currenttime, " ", data
    db.connect_to_db()
    db.insert_noise_data(noise_id, data, db.get_shift())
    db.close_db()
    global running
    if running:
        t = threading.Timer(sleeptime, insert_data)
        t.start()
	running = False
    else:
        print "System exit"
        exit = True

running = True
exit = False
data = 0

try:
    # initialize database reader
    db = ISensitGWMysql()
    sleeptime = db.sleeptime
    noise_id = db.config_data.get_noise_id()
   # print(sleeptime)
#    db.connect_to_db()
except Exception as e:
    print("Error in initializing db, reason: ", str(e))
    exit(-1)

dev = usb.core.find(idVendor = 0x16c0, idProduct=0x5dc)
assert dev is not None

t = threading.Timer(sleeptime, insert_data)
t.start()

#print dev

#print hex(dev.idVendor) + ',' + hex(dev.idProduct)

#mytime = time.strftime("%d-%m-%Y_%H:%M")

while not exit:
    running = True
    data = read_data()
    time.sleep(4.0)

#db.close_db()

