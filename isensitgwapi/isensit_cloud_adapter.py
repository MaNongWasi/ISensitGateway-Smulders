#/usr/bin/python

import urllib3.contrib.pyopenssl
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class Data:
    def __init__(self, gateway_id, beacon_id, values):
        self.gateway_id = gateway_id;
        self.beacon_id = beacon_id;
        self.values = values
        

def postdata(self):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# disable SSLV3 certificate check , aws does not support it
    urllib3.contrib.pyopenssl.inject_into_urllib3()
# no verification

   # r = requests.get("https://c81gerx5xh.execute-api.eu-central-1.amazonaws.com/beta/gateway", verify = False)
   # print (r.text)

    datax = {
        "gatewayID": self.gateway_id,
        "device": self.beacon_id, 
        "values": self.values
        }
    
    n = json.dumps(datax)
    jsons = json.loads(n)
    print (datax)
    r = requests.post('https://lk9lsgdzih.execute-api.eu-central-1.amazonaws.com/beta/gateway', n)
    print (r.text)


