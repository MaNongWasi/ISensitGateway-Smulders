import datetime
import sys
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_dynamo import *
from isensit_sql import *

device = "Acc"
table_name = "rssi_table"

def current(created_at):
    currenttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return currenttime > created_at

def upload_data():
    try:
	db.connect_to_db()
	data = db.read_rssi_data()
	if data is None:
	    print("No data left")
	else:
#	    row = 0
	    row = dydb.insert_rssi_data(data)
#	    count = 0
#	    for d in data:
#		count = count+1
#	        row_count = d["row_count"]
#	        id = d["beacon_id"]
#	        rssi_avr = d["rssi"]
#	        created_at = d["created_at"]
#	        print id, rssi_avr, created_at
#    	        dydb.insert_rssi_data(str(id), rssi_avr, created_at)
#		if count > 500:
#		    count = 0
#		    row = row_count
#  		    print "deleteing"
	    db.delete_rssi_data(row)
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
#    if db.working():
#	if db.half_hour():
     upload_data()
#        else:
#	    print("not half hour")
#	    time.sleep(60)
#    else:
#	print("not working hour")
#  	time.sleep(60)

