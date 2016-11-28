#!/usr/bin/python
import sys
# adding api to path
api_folder = "/home/pi/ISensitGateway/isensitgwapi/" 
if api_folder not in sys.path:
    sys.path.insert(0, api_folder) 
from isensit_device_adapter import * 
from lib.blescan import * 
import bluetooth._bluetooth as bluez 
from isensit_sql import * 
import time 
import threading 
import datetime 

dev_id = 0 
rssi = 0
cal_pitch = 0 
total_lift = 0 
bad_lift = 0
row_count = 0 
table_name = "acc_beacon_table"

def get_lift(beacon_id, accx, accy, accz, rssi, num):
    levelPitch = 0
    levelRoll = 0

    db.connect_to_db()
    user_cal = db.read_cal_val(beacon_id)
    if user_cal is None:
        cal_pitch = 0
        cal_roll = 0
    else:
	cal_pitch = user_cal["pitch_cal"]
	cal_roll = user_cal["roll_cal"]

#    pitch = getPitch(accx, accy, accz, cal_pitch)
#    roll = getRoll(accx, accy, accz, cal_roll)
    acc_sum = getAccSum(accx, accy, accz)

    if sqrt(pow(accx,2)+pow(accy,2)) == 0 :	
	pitch = 180
    else:
	pitch = getPitch(accx, accy, accz, cal_pitch)

    if sqrt(pow(accz,2)+pow(accx,2)) == 0 :
	    roll = 180
    else:    
	    roll = getRoll(accx, accy, accz, cal_roll)
#    print(sqrt(pow(accz,2)+pow(accx,2)))

    if pitch >= -5 and pitch <= 20:
	levelPitch = 1
    elif pitch > 20 and pitch <= 60:
	levelPitch = 2
    elif abs(pitch) > 60:
	levelPitch = 3
    elif pitch < -5 and pitch > -60:
	levelPitch = 4

    if abs(roll) <= 10:
	levelRoll = 1
    elif roll > 10 and roll <= 20:
	levelRoll = 2
    elif roll >= -20 and roll < -10:
	levelRoll = 3
    elif roll > 20:
	levelRoll = 4
    elif roll < -20:
	levelRoll = 5
 
    print(levelPitch, levelRoll)

    global pitchLevel
    global rollLevel
    currenttime = datetime.datetime.now()

    old_json = db.read_last_acc_beacon_data(table_name, beacon_id)
#    print currenttime.strftime("%Y-%m-%d")
#    print old_json['created_at'].split(" ")[0]
    if old_json is None:
	pitchList = [0, 0, 0, 0]
	rollList = [0, 0, 0, 0, 0]
 	teller = 0
    elif old_json['created_at'].split(" ")[0] is not currenttime.strftime("%Y-%m-%d"):
	pitchList = [0, 0, 0, 0]
        rollList = [0, 0, 0, 0, 0]
        teller = 0
    else:
	pitchList = [old_json["levelPitch1"], old_json["levelPitch2"], old_json["levelPitch3"], old_json["levelPitch4"]]
	rollList = [old_json["levelRoll1"], old_json["levelRoll2"], old_json["levelRoll3"], old_json["levelRoll4"],  old_json["levelRoll5"]]
	teller = old_json["teller"]
	    
    if acc_sum > 0.1 and acc_sum < 3:
        teller = teller + 1

    if levelPitch > 0:
        pitchList[levelPitch - 1] = pitchList[levelPitch - 1] + 1
    if levelRoll > 0:
	rollList[levelRoll - 1] = rollList[levelRoll - 1] + 1    
    
    print("num :", num)
    print("id : ", beacon_id)
    print("teller : ", teller)

    db.insert_acc_pitch_roll_data(beacon_id, accx, accy, accz, rssi, currenttime, acc_sum, pitch, roll, levelPitch, levelRoll, pitchList, rollList, teller, num)
    db.close_db()
#    print currenttime
    
def get_degree(r):
    if "device_info" in r and "values" in r:
	if "ID" in r["device_info"] and "ACCX" in r["values"] and "ACCY" in r["values"] and "ACCZ" in r["values"] and "RSSI" in r["values"]:
    	    id = r["device_info"]["ID"][0]
            accx = float(r["values"]["ACCX"][0])
            accy = float(r["values"]["ACCY"][0])
            accz = float(r["values"]["ACCZ"][0])
            rssi = r["values"]["RSSI"][0]
	    num = r["values"]["NUM"][0]

	    get_lift(int(id.strip('\0')), accx, accy, accz, rssi, num) 


sock = hci_start_scan(dev_id) 
try:
    # initialize database reader
    db = ISensitGWMysql()
#    db.connect_to_db()
#    total_count = db.read_acc_beacon_total_count()
#    if total_count is None:
#	total_count = 0
#    db.close_db()
  #  sleeptime = db.sleeptime
   # print(sleeptime)
except Exception as e:
    print("Error in initializing db, reason: ", str(e))
    running = False
    exit(-1)

while True:
    returnedList = parse_events(sock)
    if returnedList is not None:
	if returnedList is not False:
#	    if "782" in returnedList["device_info"]["ID"][0]:
		get_degree(returnedList)
# time.sleep(1)
