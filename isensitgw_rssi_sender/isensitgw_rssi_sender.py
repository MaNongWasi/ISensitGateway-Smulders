import datetime
import sys
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_dynamo import *
from isensit_sql import *

device = "Acc"
table_name = "rssi_table"

def working():
    currenttime = datetime.datetime.now()
    currentdate = currenttime.strftime("%Y-%m-%d")
    start_t = datetime.datetime.strptime(currentdate + start_time, "%Y-%m-%d %H:%M:%S")
    end_t = datetime.datetime.strptime(currentdate + end_time, "%Y-%m-%d %H:%M:%S")
    today = currenttime.weekday()
    return True

def current(created_at):
    currenttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return currenttime > created_at

def upload_data():
    try:
	db.connect_to_db()
	data = db.read_first_data(table_name)
	if data is None:
	    print("No data left")
	else:
	    row_count = data["row_count"]
	    id = data["beacon_id"]
	    rssi_avr = data["rssi"]
	    created_at = data["created_at"]
	    print id, rssi_avr, created_at
    	    dydb.insert_rssi_data(str(id), rssi_avr, created_at)
  	    db.delete_data(table_name, row_count)
    except Exception as e:
	print("Error in Aws Sender, reason: ", str(e))
    else:
	db.close_db()

try:
    db = ISensitGWMysql()
    start_time = db.config_data.get_start_time()
    end_time = db.config_data.get_end_time()
    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_person(), device)
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))

while True:
    if working():
	if half_hour():
            upload_data()
        else:
	    print("not half hour")
	    time.sleep(60)
    else:
	print("not working hour")
   	time.sleep(60)

