import sys
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_sql import *
from isensit_dynamo import *

device = "Acc"
gateways = ["SMULDERS_GW_001", "SMULDERS_GW_002", "SMULDERS_GW_003", "SMULDERS_GW_004"]
beacons = ["3037"]

def get_limit_time(id):
    created_at = get_created_at_time(id)
    if created_at is not None:
        time = created_at.split(":")
        second = time[2]
        if second > 30:
            minute = str(int(time[1]) + 1)
            if minute < 10:
                minute = "0" + minute
            limit_time = time[0] + ":" + minute + ":00"
        else:
    	    limit_time = time[0] + ":30:00"
        return limit_time

def half_hour():
    currenttime = datetime.datetime.now()
    return currenttime.minute == 00 or currenttime.minute == 30

def working():
    currenttime = datetime.datetime.now()
    currentdate = currenttime.strftime("%Y-%m-%d")
    start_t = datetime.datetime.strptime(currentdate + start_time, "%Y-%m-%d %H:%M:%S")
    end_t = datetime.datetime.strptime(currentdate + end_time, "%Y-%m-%d %H:%M:%S")
    today = currenttime.weekday()
    return True 

def get_created_at_time(id):
    return dydb.get_created_at_item(id)

def upload_data(id, created_at):    
    if created_at is not None:
        returned_items = dydb.get_rssi_item(id, created_at)
        if returned_items is not None:
            item_info = {}
            rssi_max = -1000
            for item in returned_items:
            	if 'rssi' in item and 'gatewayID' in item:
                    rssi = item['rssi']
                    if rssi > rssi_max:
                    	rssi_max = rssi
                    	item_info = item
            print(item_info)
	    if "gatewayID" in item_info and "created_at" in item_info and "rssi" in item_info:
                succeed = dydb.insert_rssi_total(id, item_info)
        	if succeed:
                    dydb.delete_rssi_item(id, created_at)



try:
    db = ISensitGWMysql()
    start_time = db.config_data.get_start_time()
    end_time = db.config_data.get_end_time()
    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_person, device)
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))


while True:
    if working():
	if half_hour():
            for id in beacons:
	  	time_end = get_limit_time(id)
	  	created_at = get_created_at_time(id)
		print created_at 
		while created_at is not None and created_at < time_end:
    		    upload_data(id, created_at)
    		    created_at = get_created_at_time(id)
        else:
	    print("not working hour")
	    time.sleep(60)
    else:
	print("not working hour")

 
    
