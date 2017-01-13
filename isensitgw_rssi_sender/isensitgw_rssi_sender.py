import datetime
import sys
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_dynamo import *
from isensit_sql import *

device = "Acc"
table_name = "rssi_table"
shift = 0

def current(created_at):
    currenttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return currenttime > created_at

def upload_data():
    global shift
    try:
	db.connect_to_db()
	data = db.read_rssi_data()
	if data is None:
	    print("No data left")
	else:
	    print data[len(data)-1]["row_count"]
	    row_count = data[len(data)-1]["row_count"]
#	    print "row count " , row_count
#	    id = str(data["beacon_id"])
#	    rssi_avr = data["rssi"]
#	    created_at = data["created_at"]
#	    print id, rssi_avr, created_at
	    dydb.insert_rssi_data(data)
#  	    upload = dydb.insert_rssi_data(data)
#	    dydb.update_rssi_data(data, gw)
#	    if upload:
#	    	print "yesupload "
#  	    	db.delete_rssi_data(row_count+1)
            db.delete_rssi_data(row_count+1)
    except Exception as e:
	print("Error in Aws Sender, reason: ", str(e))
    else:
	db.close_db()

try:
    db = ISensitGWMysql()
    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_person(), device)
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))

while True:
    shift = db.get_shift()
    if shift != 0:
#    if db.working():
	upload_data()
#	if db.half_hour():
#            upload_data()
#        else:
#	    print("not half hour")
#	    time.sleep(60)
    else:
	print("not working hour")
   	time.sleep(60)
