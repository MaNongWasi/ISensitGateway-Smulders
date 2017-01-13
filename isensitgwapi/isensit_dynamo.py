from __future__ import print_function # Python 2/3 compatibility
import boto3
import time
from boto3 import dynamodb
from boto3.session import Session
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import csv, json, sys, decimal, logging
from decimal import *
import datetime

class ISensitDynamodb():
#    def __init__(self, gatewayID, table_name, total_table_name, person_table_name, device):
    def __init__(self, gatewayID, table_name, person_table_name, device):
    	self.dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
    	self.gatewayID = gatewayID
    	self.table = self.dynamodb.Table(table_name)
#    	self.table_save = self.dynamodb.Table(total_table_name)
	self.table_person = self.dynamodb.Table(person_table_name)
	self.device = device    
	self.table_rssi = self.dynamodb.Table("ISensitRSSI")
 	self.table_rssi_total = self.dynamodb.Table("ISensitRSSITotal")
	self.gateways = ["SMULDERS_GW_001", "SMULDERS_GW_002", "SMULDERS_GW_003", "SMULDERS_GW_004"]

    def get_item(self, created_at, shift):
	currenttime = datetime.datetime.strptime(created_at,'%Y-%m-%d %H:%M:%S')
    	try:
	    response = self.table_person.get_item(
	    	Key={
                    'created_at': currenttime.strftime("%Y-%m-%d") + " " + self.gatewayID + " " + str(shift),
                    'deviceID': self.device
            	}
	    )

        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            if 'Item' in response:
            	item = response['Item']
            	print("GetItem succeeded:")
            	print(json.dumps(item, indent=4, cls=DecimalEncoder))
            	return item

            else:
            	print("Empty set")
            	return None

    def insert_to_next_table(self, deviceInfoDict, deviceValueDict):
        epoch_time = Decimal(time.time()).quantize(Decimal("0"))
    	total_item = {
            "gatewayID": self.gatewayID,
            "device_type": self.device,
#            "timestamp": epoch_time,
            "device": deviceInfoDict,
            "values": deviceValueDict,
        }
        with self.table_save.batch_writer() as batch:
            print(total_item)
            batch.put_item(total_item)
#    	table_save.batch_writer().put_item(total_item)
    	print("item_total", total_item)


    def insert_data(self, created_at, deviceInfoDict, deviceValueDict):
#        epoch_time = Decimal(time.time()).quantize(Decimal("0"))
	currenttime = str(datetime.datetime.now())
        Item = {
                'gatewayID':self.gatewayID,
	 	'device_type':self.device,
#                'timestamp':Decimal(time.time()).quantize(Decimal("0.01")),
		'upload_at': currenttime,
                'device': deviceInfoDict,
                'values': deviceValueDict,
        }

        with self.table.batch_writer() as batch:
            print("item ", Item)
            batch.put_item(Item)

    def insert_user_data(self, deviceID, deviceInfoDict, deviceValueDict, created_at, shift):
#        epoch_time = Decimal(time.time()).quantize(Decimal("0"))
	upload_at = str(datetime.datetime.now())
  	currenttime = datetime.datetime.strptime(created_at,'%Y-%m-%d %H:%M:%S') #.%f')
	print ("------------------------currenttimt ", currenttime)
        Item_person = {
                'deviceID': deviceID,
                'gatewayID':self.gatewayID,
		'upload_at': upload_at, 
		'created_at': currenttime.strftime("%Y-%m-%d") + " " + self.gatewayID + " " + str(shift),
                'device': deviceInfoDict,
                'values': deviceValueDict,
        }

        with self.table_person.batch_writer() as batch:
            print("item_person ", Item_person)
            batch.put_item(Item_person)

    def insert_rssi_data(self, data):
	row = 0
	with self.table_rssi.batch_writer() as batch:
 	    for d in data:
                Item_rssi = {
                    'deviceID': str(d["beacon_id"]),
	            'gatewayID': self.gatewayID,
	            'upload_at': str(datetime.datetime.now()),
	            'rssi': d["rssi"],
	            'timestamp': d["created_at"] + "/" + self.gatewayID,
	            'created_at': d["created_at"],
	        }

	        print("item_rssi ", Item_rssi)
	        batch.put_item(Item_rssi)

    def get_created_at_item(self, deviceID):
        try:
            query = Key('deviceID').eq(deviceID)
            prj_exp = "#created_at"
            prj_attr={ "#created_at":"created_at"}
            response = self.table_rssi.query(
                ProjectionExpression=prj_exp,
                ExpressionAttributeNames=prj_attr,
                KeyConditionExpression=query,
                Limit=1,
                ScanIndexForward=False,
                )
        except ClientError as e:
            print(e.response['Eorror']['Message'])
        else:
            if 'Count' in response:
                if(response['Count'] > 0):
                    if('Items' in response):
                        return response['Items'][0]['created_at']
                    else:
                        print("No Items in response")
                        return None
                else:
                    print("Empty Set")
                    return None
            else:
                print("No response")
                return None

    def get_rssi_item(self, deviceID, created_at):
        try:
            query = Key('deviceID').eq(deviceID) & Key('created_at').lt(created_at)
            prj_exp = "#gw1, #gw2, #gw3, #gw4, #created_at"
            prj_attr = {"#gw1": "GW1", "#gw2":"GW2", "#gw3": "GW3", "#gw4":"GW4", "#created_at":"created_at"}
            response = self.table_rssi.query(
                ProjectionExpression=prj_exp,
                ExpressionAttributeNames=prj_attr,
                KeyConditionExpression=query,
                ScanIndexForward=False,
            )

        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            if 'Count' in response:
                if response['Count'] > 0:
                    if('Items' in response):
                        return response['Items']
                    else:
                        print("No Items in response")
                        return None
                else:
                    print("Empty Set")
                    return None
            else:
	 	print("No response")
                return None

    def insert_rssi_total(self, deviceID, data):
        upload_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            Item_rssi_total = {
                'deviceID': deviceID,
                'gatewayID':data['gatewayID'],
                'upload_at': upload_at,
                'created_at': data['created_at'],
                'rssi': data['rssi'],
            }

            with self.table_rssi_total.batch_writer() as batch:
                print("item ", Item_rssi_total)
                batch.put_item(Item_rssi_total)
        except ClientError as e:
            print (e.response['Error']['Message'])
            return False
        else:
            return True

    def insert_rssi_total2(self, deviceID, data, created_at):
         upload_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         try:
             Item_rssi_total = {
                 'deviceID': deviceID,
                 'GW1':data['GW1'],
                 'GW2':data['GW2'],
                 'GW3':data['GW3'],
                 'GW4':data['GW4'],
                 'upload_at': upload_at,
                 'created_at': created_at,
             }
             with self.table_rssi_total.batch_writer() as batch:
                 print("item ", Item_rssi_total)
                 batch.put_item(Item_rssi_total)
         except ClientError as e:
             print (e.response['Error']['Message'])
             return False
         else:
             return True

    def delete_rssi_item(self, deviceID, created_at):
            try:
                delete_item = {
                    'deviceID': deviceID,
                    'created_at': created_at
                }
#                print(delete_item)
                with self.table_rssi.batch_writer() as batch:
                    batch.delete_item(delete_item)

            except ClientError as e:
                print (e.response['Error']['Message'])
            else:
                print("Delete Item succeed")
#                print(json.dumps(response, indent = 4, cls = DecimalEncoder))


    def update_rssi_data(self, data, gatewayID):
	row = 0
	try:
	    for d in data:
	  	print(d)
	        self.table_rssi.update_item(
	            Key={
		        'deviceID': str(d["beacon_id"]),
		        'created_at': d["created_at"]
	            },
	            UpdateExpression='SET ' + gatewayID + ' =:val',
	            ExpressionAttributeValues={
		        ':val': d["rssi"]
	            }
	        )
	except ClientError as e:
	    print (e.response['Error']['Message'])
	else:
	    print("update Item succeed")
	    if row < d["row_count"]:
	        row = d["row_count"]
	    return row

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

