
import sys
import threading
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_dynamo import *
from isensit_sql import *


device = "Acc"
sleeptime = 5.0 # maybe let it depend on db amount
pre_t = {}
cur_t = {}
ids = []

def current(created_at):
    currenttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return currenttime > created_at

def get_earliest_time():
    global ids
    time_dict = {}
    try:
  	db.connect_to_db()
	data = db.read_distinct_acc_beacon_data("acc_sensors")
        if data is None:
            print("No data left")
        else:
	    for beacon_id in data:
		id = beacon_id['beacon_id']
		ids.append(id)
		created_at = str(db.read_earliest_acc_beacon_data(id)['created_at'])
		if created_at is not None:
	    	    time_dict[id] = created_at
		else:
	    	    time_dict[id] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#		    print "timedict", time_dict[id]
    except Exception as e:
	print("Error in geting time dict, reason: ", str(e))
    else:
	db.close_db()
        return time_dict

def check_time():
    global pre_t
#    if db.working():
    pre_t.clear()
    pre_t = get_earliest_time()
    print "pre_t ",pre_t
    if len(pre_t) > 0:
        upload_data(pre_t)
    else:
        print "No time data left"
    t = threading.Timer(sleeptime, check_time)
    t.start()

def upload_data(pre_time):
    global ids
    try:
	if len(ids) > 0:
	    db.connect_to_db()
            for beacon_id in ids:
	        rssi_avr = 0
		pre = pre_time[beacon_id]
		print "personpre ", pre
		cur = datetime.datetime.strptime(pre, "%Y-%m-%d %H:%M:%S")+datetime.timedelta(seconds = 5)
		cur = str(cur)
		print "precure ",cur
	        d = db.read_earliest_acc_beacon_datas(beacon_id, pre)
		print d
		if d is not None:
		    print len(d)
		    for rssi in d:
		        print "rssi ", rssi["beacon_rssi"]
		        rssi_avr = rssi_avr + rssi["beacon_rssi"]
 	            rssi_avr = rssi_avr / len(d)
	            print "avr ", rssi_avr
 		    db.insert_rssi_data(beacon_id, rssi_avr, cur)
		    db.delete_earliest_beacon_data(beacon_id, pre, cur)
    except Exception as e:
	print("Error in Aws Sender, reason: ", str(e))
    else:
	db.close_db()

try:
    db = ISensitGWMysql()
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))

t = threading.Timer(sleeptime, check_time)
t.start()

#while True:
#    if db.working():
#        upload_data()
#    else:
#	print("not working hour")
#	time.sleep(60)
