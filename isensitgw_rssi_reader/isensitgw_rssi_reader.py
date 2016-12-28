import datetime
import sys
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_dynamo import *
from isensit_sql import *

device = "Acc"

def current(created_at):
    currenttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return currenttime > created_at

def upload_data():
    try:
	db.connect_to_db()
	data = db.read_distinct_acc_beacon_data()
	if data is None:
	    print("No data left")
	else:
	    for beacon_id in data:
	        rssi_avr = 0
		id = beacon_id.values()[0]
	 	if id is not None:
		    print id
		    created_time = db.read_earliest_acc_beacon_data(id)
		    if created_time is not None:
			created_at = created_time["created_at"]
			if current(created_at):
			    print created_at
 		            d = db.read_earliest_acc_beacon_datas(id, created_at)
		            if d is not None:
#		    		print len(d)
		    	        for rssi in d:
#		 	            print "rssi ", rssi["beacon_rssi"]
		                    rssi_avr = rssi_avr + rssi["beacon_rssi"]
 	                        rssi_avr = rssi_avr / len(d)
#		    	    print "avr ", rssi_avr
		    	    db.insert_rssi_data(str(id), rssi_avr, str(created_at))
		 	    next_data = db.read_next_acc_beacon_data(id, created_at)
			    if next_data is not None:
				db.delete_earliest_beacon_data(id, created_at)
    except Exception as e:
	print("Error in Aws Sender, reason: ", str(e))
    else:
	db.close_db()

try:
    db = ISensitGWMysql()
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))

while True:
    if db.working():
        upload_data()
    else:
	print("not working hour")
	time.sleep(60)
