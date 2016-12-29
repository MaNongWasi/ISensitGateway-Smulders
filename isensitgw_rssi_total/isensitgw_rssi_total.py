import sys
api_folder = "/home/ubuntu/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_sql import *
from isensit_dynamo import *
device = "Acc"
gws = ["GW1", "GW2", "GW3", "GW4", "GW5"]
beacons = ["3262", "13591", "5833", "13576", "12931","13305","13320","13500", "13560","13606" ]
gw_dict = {}

def upload_data(id, created_at):
    table_name = "maxrssi_table"
    db.connect_to_db()

    if created_at is not None:
        returned_items = dydb.get_rssi_item(id, created_at)
#	print returned_items

	old_json=db.read_last_acc_beacon_data(table_name,id)
	if old_json is None:
	    print "no old data"
	    row_count = 0
	    for gw in gws:
		gw_dict[gw] = 0
	else:
	    row_count = old_json["row_count"]
	    for gw in gws:
		gw_dict[gw] = old_json[gw]
	    print "gw_dict " , gw_dict


        if returned_items is not None:
	    for item in returned_items:
		print "ITEMT ", item
		currentt = item['created_at']
       		item_info = gws[4]
            	rssi_max = -1000
		for gw in gws:
		    if gw in item:
			rssi = item[gw]
			if rssi > rssi_max:
			    rssi_max = rssi
			    print 'rssi max ', rssi_max
			    item_info = gw
			    print "item_info", item_info
		gw_dict[item_info] = gw_dict[item_info] + 1
#            	if 'rssi' in item and 'gatewayID' in item:
#                    rssi = item['rssi']
#                    if rssi > rssi_max:
#                    	rssi_max = rssi
#			print 'rssi max ', rssi_max
#                    	item_info = item["gatewayID"]
#			print "item_info", item_info
#	    if item_info == "SMULDERS_GW_001":
#		GW1 = GW1 +1
#	    elif item_info == "SMULDERS_GW_002":
#		GW2 = GW1+1
#	    elif item_info == "SMULDERS_GW_003":
#		GW3 = GW3+1
#	    elif item_info == "SMULDERS_GW_004":
#		GW4 = GW4+1
#		print "GW4 after ", GW4
	        dydb.insert_rssi_total2(id, gw_dict, currentt)
	        dydb.delete_rssi_item(id, currentt)
            db.insert_max_rssi(id, currentt, gw_dict)
	    db.delete_acc_beacon_data(table_name,id,row_count)

	    db.close_db()
#            print(item_info)
#	    if "gatewayID" in item_info and "created_at" in item_info and "rssi" in item_info:
#                succeed = dydb.insert_rssi_total(id, item_info)



try:
    db = ISensitGWMysql()
    start_time = db.config_data.get_start_time()
    end_time = db.config_data.get_end_time()
    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_person, device)
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))


while True:
    if db.working():
	if db.half_hour():
 	    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for id in beacons:
  	        upload_data(id, created_at)
	    time.sleep(60)
        else:
	    print("not working hour")
	    time.sleep(60)
    else:
	print("not working hour")



