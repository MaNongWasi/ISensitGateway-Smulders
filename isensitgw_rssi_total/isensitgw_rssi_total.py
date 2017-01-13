import sys
api_folder = "/home/ubuntu/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_sql import *
from isensit_dynamo import *

device = "Acc"
gws = ["GW1", "GW2", "GW3", "GW4", "GW5"]
beacons = ["13653", "3262", "13591", "3890","3037","13335","13515","5883","13529","13607","13729","3063","2687","2834","2730", "5833", "13576", "12931","13305","13320","13500", "13560","13606" ]
gw_dict = {}
rssi_table = "rssi_total_table"
table_name = "maxrssi_table"

def upload_data(id, created_at,start_t):
    shift = 0
    db.connect_to_db()

    if created_at is not None:
        returned_items = dydb.get_rssi_item(id, created_at)

	print "id", id
#	print returned_items

        if returned_items is not None:
	    db.update_rssi_total(id, returned_items, start_t, created_at)
	    items = db.read_all_data(rssi_table)
#	    print "itemts ", items
	    if items is not None:
	        for item in items:
#		    print "ITEMT ", item
		    currentt = str(item['created_at'])
		    shift = db.get_shift_nr(datetime.datetime.strptime(currentt, "%Y-%m-%d %H:%M:%S"))

		    old_json=db.read_last_acc_beacon_data(table_name,id, shift)
	            if old_json is None:
                 	print "no old data"
#            		row_count = 0
            		for gw in gws:
                	    gw_dict[gw] = 0
        	    else:
#            		row_count = old_json["row_count"]
            		for gw in gws:
                	    gw_dict[gw] = old_json[gw]
#        	    print "gw_dict " , gw_dict

       		    item_info = gws[4]
            	    rssi_max = -1000
		    for gw in gws:
		    	if gw in item:
			    rssi = item[gw]
			    if rssi > rssi_max:
			    	rssi_max = rssi
#			    	print 'rssi max ', rssi_max
			    	item_info = gw
#			    	print "item_info", item_info
		    gw_dict[item_info] = gw_dict[item_info] + 1
   		    print "GW DICT ", gw_dict
                    db.insert_max_rssi(id, currentt, gw_dict, shift)


                if dydb.insert_rssi_total(id, gw_dict, created_at, shift):
#	            dydb.delete_rssi_item(id, returned_items)
#	            db.delete_acc_beacon_data(table_name,id,row_count) # also delete all data?
	            db.delete_all_data(rssi_table)

    db.close_db()



try:
    db = ISensitGWMysql()
#    start_time = db.config_data.get_start_time()
#    end_time = db.config_data.get_end_time()
    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_person, device)
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))


#while True:
#    if db.working():
if db.half_hour():
    currentt = datetime.datetime.now()
    created_at = currentt.strftime("%Y-%m-%d %H:%M:%S")
    start_t = currentt - datetime.timedelta(minutes=30)
    start_t = start_t.strftime("%Y-%m-%d %H:%M:%S")
    print "created_at",created_at
    print "start_t ",start_t
    for id in beacons:
        upload_data(id, created_at,start_t)
#        time.sleep(60)
##       else:
##	    print("not working hour")
##	    time.sleep(60)
#    else:
#	print("not working hour")

#start_t = "2017-01-12 13:50:00"
#created_at = "2017-01-13 13:45:20"
#for id in beacons:
#    upload_data(id, created_at,start_t)
