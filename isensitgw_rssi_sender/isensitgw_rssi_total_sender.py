#from __future__ import print_function # Python 2/3 compatibility
import time
from decimal import *
import sys
import datetime

# adding api to path
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_sql import *
from isensit_dynamo import *
import datetime

deviceInfoDict = {}
deviceValueDict = {}
row_count = 0
DATA = {}

data = None
count = 0
table_name = "maxrssi_table"
device = "Acc"

#while True:
def upload_data():
    try:
    	db.connect_to_db()
    	data = db.read_distinct_rssi_data()
    	print "ids", data
    	if data is None:
            print("No data left")
    	else:
	    for beacon_id in data:
	        id = beacon_id.values()[0]
	        if id is not None:
	            d = db.read_last_acc_beacon_data(table_name, id)
		    print(d)
                    row_count = d["row_count"]
#                    deviceInfoDict['ID'] = str(d["beacon_id"])
             	    DATA['GW1'] = d['GW1']
		    DATA['GW2'] = d['GW2']
                    DATA['GW3'] = d['GW3']
                    DATA['GW4'] = d['GW4']
	  	    DATA['upload_at'] = str(datetime.datetime.now())
		    DATA['created_at'] = str(d['created_at'])
		
		    dydb.insert_rssi_total2(str(id), DATA)		
		    db.delete_acc_beacon_data(table_name, id, row_count)
       	 	    print("upload successful, deleting row..")
		   	
    except Exception as e:
        print("Error in rssitotal Sender, reason: ", str(e))
    else:
#        if data is not None:
#            print("uploading...")
#            upload = uploader.post_data(jsonDict)

#            if upload:
#                print("upload successful, deleting row..")
#                db.delete_data(table_name, row_count)

#            else:
#                print("Data was not uploaded reason: ")
#                print(upload)
        db.close_db()


try:
    db = ISensitGWMysql()
#    print(db.config_data.get_dynamodb_table_person())
#    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_save(), db.config_data.get_dynamodb_table_person(), device)
    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_person(), device)
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))

while True:
    if db.working():
#	upload_data()
#	time.sleep(1)
	if db.half_hour():
            upload_data()
	else:
	    print("not half hour")
	    time.sleep(60)
    else:
        print("not working hour")

