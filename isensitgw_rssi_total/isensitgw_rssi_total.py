import sys
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_sql import *
from isensit_dynamo import *

device = "Acc"
gateways = ["SMULDERS_GW_001", "SMULDERS_GW_002", "SMULDERS_GW_003", "SMULDERS_GW_004"]
beacons = ["3262", "13591", "5833", "13576", "12931","13305","13320","13500", "13560","13606" ]

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


def get_created_at_time(id):
    return dydb.get_created_at_item(id)

def upload_data(id, created_at):
    table_name = "maxrssi_table"     
    db.connect_to_db()

    if created_at is not None:	
        returned_items = dydb.get_rssi_item(id, created_at)
	old_json=db.read_last_acc_beacon_data(table_name,id)
	if old_json is None:
	    print "no old data"  
	    row_count = 0
	    GW1=0
	    GW2=0
	    GW3=0
	    GW4=0
	else:
	    row_count = old_json["row_count"]
	    GW1 = old_json["GW1"]
	    GW2 = old_json["GW2"]
	    GW3 = old_json["GW3"]
	    GW4 = old_json["GW4"]
	    print "GW1" , GW1
	    print "GW4" , GW4

		
	
        if returned_items is not None:
	    currentt = created_at
            item_info = {}
            rssi_max = -1000
            for item in returned_items:
            	if 'rssi' in item and 'gatewayID' in item:
                    rssi = item['rssi']
                    if rssi > rssi_max:
                    	rssi_max = rssi
			print 'rssi max ', rssi_max 
                    	item_info = item["gatewayID"]
			print "item_info", item_info
	    if item_info == "SMULDERS_GW_001":
		GW1 = GW1 +1
	    elif item_info == "SMULDERS_GW_002":
		GW2 = GW1+1
	    elif item_info == "SMULDERS_GW_003":
		GW3 = GW3+1
	    elif item_info == "SMULDERS_GW_004":
		GW4 = GW4+1
		print "GW4 after ", GW4

	    succeed = db.insert_max_rssi(id, currentt, GW1, GW2, GW3, GW4)
	    db.delete_acc_beacon_data(table_name,id,row_count)
	    dydb.delete_rssi_item(id, created_at)
	    db.close_db	 
#            print(item_info)
#	    if "gatewayID" in item_info and "created_at" in item_info and "rssi" in item_info:
#                succeed = dydb.insert_rssi_total(id, item_info)
#        	if succeed:



try:
    db = ISensitGWMysql()
    start_time = db.config_data.get_start_time()
    end_time = db.config_data.get_end_time()
    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_person, device)
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))


while True:
    if db.working():
#	if db.half_hour():
        for id in beacons:
	    time_end = get_limit_time(id)
	    created_at = get_created_at_time(id)
	    print "creted_at", created_at 
	    while created_at is not None and created_at < time_end:
    		upload_data(id, created_at)
    		created_at = get_created_at_time(id)
#        else:
#	    print("not working hour")
#	    time.sleep(60)
    else:
	print("not working hour")

 
    

