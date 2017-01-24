import datetime
import sys
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_dynamo import *
from isensit_sql import *

device = "Acc"

def current(created_at):
    currenttime = datetime.datetime.now()
    created2 = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
    return created2 > (currenttime - datetime.timedelta(0,5))

def upload_data():
    try:
	db.connect_to_db()
	data = db.read_distinct_acc_beacon_data("acc_beacons")
	if data is None:
	    print("No data left")
	else:
	    shift = db.get_shift()
	    for beacon_id in data:
	        rssi_avr = 0
		rssi = 0
		id = str(beacon_id.values()[0])
	 	if id is not None:
		    print id
		    created_time = db.read_earliest_acc_beacon_data(id,shift)
		    if created_time is not None:
			created_at = created_time["created_at"]
			print("crtime", created_at)
			if current(created_at):
 		            d = db.read_earliest_acc_beacon_datas(id, created_at)
			    print("d", d)
		            if d is not None:
				rssi = d[0]["beacon_rssi"]
			  	db.insert_rssi_data(id, rssi, str(created_at))
				print("rssi", rssi)
    except Exception as e:
	print("Error in Aws Sender, reason: ", str(e))
    else:
	db.close_db()

try:
    db = ISensitGWMysql()
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))

while True:
#    if db.working():
    upload_data()
    time.sleep(5)
#    else:
#	print("not working hour")
#	time.sleep(60)

