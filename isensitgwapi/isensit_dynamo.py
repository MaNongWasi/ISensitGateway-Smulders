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

    def get_item(self, created_at):
	currenttime = datetime.datetime.strptime(created_at,'%Y-%m-%d %H:%M:%S')
    	try:
	    response = self.table_person.get_item(
	    	Key={
                    'created_at': currenttime.strftime("%Y-%m-%d") + " " + self.gatewayID,
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

    def insert_user_data(self, deviceID, deviceInfoDict, deviceValueDict, created_at):
#        epoch_time = Decimal(time.time()).quantize(Decimal("0"))
	upload_at = str(datetime.datetime.now())
  	currenttime = datetime.datetime.strptime(created_at,'%Y-%m-%d %H:%M:%S') #.%f')
	print ("------------------------currenttimt ", currenttime)
        Item_person = {
                'deviceID': deviceID,
                'gatewayID':self.gatewayID,
		'upload_at': upload_at, 
		'created_at': currenttime.strftime("%Y-%m-%d") + " " + self.gatewayID,
                'device': deviceInfoDict,
                'values': deviceValueDict,
        }

        with self.table_person.batch_writer() as batch:
            print("item_person ", Item_person)
            batch.put_item(Item_person)

    def insert_rssi_data(self, deviceID, rssi, created_at):
        upload_at = str(datetime.datetime.now())
        Item_rssi = {
            'deviceID': deviceID,
	    'gatewayID': self.gatewayID,
	    'upload_at': upload_at,
	    'rssi': rssi,
	    'created_at': created_at,
	}

	with self.table_rssi.batch_writer() as batch:
#	    print("item_rssi ", Item_rssi)
	    batch.put_item(Item_rssi)
	

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

