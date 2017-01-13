from __future__ import print_function # Python 2/3 compatibility
import time
from decimal import *
import sys

# adding api to path
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_sql import *
from isensit_dynamo import *

deviceInfoDict = {}
deviceValueDict = {}
row_count = 0
table_name = "fd_sensor_table"
device = "FineDust"
shift = 0

try:
    db = ISensitGWMysql()
#    print(db.config_data.get_dynamodb_table())
#    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_save(), db.config_data.get_dynamodb_table_person(), device)
    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_person(), device)
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))

#client = boto3.client('dynamodb')
while True:
    shift = db.get_shift()
    try:
        db.connect_to_db()
        data = db.read_first_data(table_name)
        if data is None:
	    print("No data left")
        else:
            row_count = data["row_count"]
            deviceInfoDict['sensor'] = device
	    deviceInfoDict['ID'] = str(data["fd_id"])
	    deviceValueDict['pm'] = Decimal(data["pm"]).quantize(Decimal("0.1"))
            deviceValueDict['temp'] = Decimal(data["temp"]).quantize(Decimal("0.01"))
            deviceValueDict['hum'] = Decimal(data["hum"]).quantize(Decimal("0.01"))
            deviceValueDict['pm_hour'] = Decimal(data["pm_hour"]).quantize(Decimal("0.1"))
	    created_at = str(data["created_at"])
            deviceValueDict['created_at'] = str(data["created_at"])
		
	    dydb.insert_data(created_at, deviceInfoDict, deviceValueDict) 	    
	
#	    if db.working():
            old_json = dydb.get_item(created_at, shift)
            print("old json ", old_json)
            if old_json is None:
                sensor_count = 0;
                sensor_db = 0;
            else:
                sensor_count = old_json["values"]["pm_count"] + 1
	        sensor_db = old_json["values"]["pm"] + deviceValueDict['pm']
	    	    
	    deviceValueDict['pm_count'] =  sensor_count
	    deviceValueDict['pm'] = sensor_db
#	        dydb.insert_to_next_table(deviceInfoDict, deviceValueDict)
	
            dydb.insert_user_data("FineDust", deviceInfoDict, deviceValueDict, created_at, shift)
    
	    db.delete_data(table_name, row_count,shift)	
    except Exception as e:
        print("Error in Aws Sender, reason: ", str(e))
    else:
        db.close_db()




