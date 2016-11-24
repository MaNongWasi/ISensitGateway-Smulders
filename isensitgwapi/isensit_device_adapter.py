import struct
from math import *

LSupportedDevices = [
    "EMBC02",  # Switzerland Beacons
    "IB001M",  # China Beacons
    "IB003N",  # China Beacons
    "WSBEACON",
    "SENSOR TAG",
    "Ghostyu Beacon",
    "Encoder",
]

# "Mode_Name": "Item", starting_pos, ending_pos, data_type, unit, device_info or value"
LDeviceMode = [
    {
        "IBeacon":
            [
                ["UUID", -22, -6, "S", " ", "DI"],
                ["RSSI", -1, 0, "R", "dBm", "V"],
                ["ID", -6, -4, "I", " ", "DI"],
                ["MAJOR", -6, -4, "I", " ", "V"],
                ["MINOR", -4, -2, "I", " ", "V"]
            ]
    },    {
        "LORAParking":
            [
                ["UUID", -22, -6, "S", " ", "DI"],
                ["RSSI", -1, 0, "AES64R", "dBm", "V"]
            ]
    },
    {
        "Sensor":
            [
                ["UUID", 10, 20, "S", " ", "DI"],
                ["ID", 20, 26, "A", " ", "DI"],
                ["RSSI", -1, 0, "R", "dBm", "V"],
                ["ACCX", -11, -10, "F", "g", "V"],
                ["ACCY", -9, -8, "F", "g", "V"],
                ["ACCZ", -7, -6, "F", "g", "V"],
                #  ["MINOR", 20, 26, "A", " ", "V"]
            ]
    },
    {
        "Encoder":
            [
                ["UUID", -7, -3, "S", " ", "DI"],
                ["ID", -11, -7, "A", " ", "DI"],
                ["RSSI", -1, 0, "R", "dBm", "V"],
                ["DEGREE", -3, -1, "F", " ", "V"]
            ]
    },
    {
        "3axisBeacons":
            [
                ["UUID", -7, -3, "S", " ", "DI"],
                ["ID", -11, -7, "A", " ", "DI"],
                ["A", -1, 0, "R", " ", "V"],
                ["B", -3, -1, "F", " ", "V"]
            ]
    },

]

# device_type: device_name
DDevice = {
    #    "699ebc80e1f311e39a0f0cf3ee3bc012": [LSupportedDevices[0], LDeviceMode[0]],
    	"0f09454d426561636f6e": [LSupportedDevices[0], LDeviceMode[2]],
        "ebefd08370a247c89837e7b5634df524" :[LSupportedDevices[1], LDeviceMode[0]],
    #    "fda50693a4e24fb1afcfc6eb07647825": [LSupportedDevices[3], LDeviceMode[0]],
    #    "e2c56db5dffb48d2b060d0f5a71096e0": [LSupportedDevices[5], LDeviceMode[0]],
    #    "05160818": [LSupportedDevices[6], LDeviceMode[2]],

}


def __init__(self):
    self.value = 0


# tested
def isSupported(device_type):
    try:
        device_info = DDevice[device_type]
    except KeyError as e:
        #        print ('Device Not Supported, I got an KeyError - reason "%s"' % str(e))
        return False
    except IndexError as e:
        #        print ('Device Not Supported, I got an IndexError - reason "%s"' % str(e))
        return False
    else:
        device_name = device_info[0]
        if (device_name in LSupportedDevices):
            # print ("Device Is Supported : ")
            # print(device_info)
            return True
        return False


# tested
def deviceStruct(device_type):
    if (isSupported(device_type)):
        try:
            device_info = DDevice[device_type]
            device_mode = device_info[1]
        except KeyError as e:
            print('Device Structure Not Found, or Mode not supported. I got an KeyError - reason "%s"' % str(e))
            return "error"
        except IndexError as e:
            print('Device Structure Not Found, or Mode not supported.I got an IndexError - reason "%s"' % str(e))
            return "error"
        else:
            for key in device_mode:
                return (device_mode[key])
    else:
        print("Device is Not Supported.")
        return "error"


def findDeviceType(sending_interface, data):
    # read the json format
    if (sending_interface == "BLESCAN"):
        for device_mode in LDeviceMode:
            # see if its a Ibeacon
            for key in device_mode:
                device_struct = device_mode[key]
                # print(device_struct)
                input = data[device_struct[0][1]: device_struct[0][2]]
                result = getString(input)
            if (isSupported(result)):
                return result


# pkt = bytes([0x13, 0x00, 0x00, 0x00, 0x08, 0x00])

def parseDeviceStruct(device_structure, pkt):
    jsonDict = {}
    deviceInfoDict = {}
    deviceValueDict = {}

    for item in device_structure:
        input = pkt[item[1]: item[2]]

        if item[3] == "S":
            result = getString(input)
        if item[3] == "AES64R":
            result = getString(input)
        if item[3] == "I":
            result = getInt(input)
        if item[3] == "F":
            result = getFloat(input, item[0])
        # if item[3] == "C":
        #     result = getChar(input)
        if item[3] == "BCD":
            result = getBCD(input)
        if item[3] == "R":
            input = pkt[item[1]]
            result = getRSSI(input)
        if item[3] == "A":
            result = getACIItoString(input)
        if item[5] == "DI":
            deviceInfoDict[item[0]] = str(result), item[4]
        if item[5] == "V":
            deviceValueDict[item[0]] = str(result), item[4]
    jsonDict["device_info"] = deviceInfoDict
    jsonDict["values"] = deviceValueDict
    return jsonDict
    # print (json.dumps(jsonDict))


def getInt(pkt):
    myInteger = 0
    multiple = 256
    for c in pkt:
        myInteger += struct.unpack("B", c)[0] * multiple
        multiple = 1
    return myInteger


def getFloat(pkt, value_type):
    # myString = "";
    myInteger = 0
    mySensor = 0
    multiple = 256
    # if(struct.unpack("B", pkt[0])[0] & 0xF0 == 0xB0):
    # myInteger = (struct.unpack("B", pkt[0])[0] & 0x07) * multiple + struct.unpack("B", pkt[1])[0];

    # myString = "%02x" %struct.unpack("B",pkt[0])[0] + "%02x" %struct.unpack("B",pkt[1])[0] + "   %d" %myInteger
    if ("ACC" in value_type):
        mySensor = getAcc(pkt)
        # myInteger = (struct.unpack("B", pkt[0])[0] & 0x07) * multiple + struct.unpack("B", pkt[1])[0];
        # if(myInteger > 1023):
        # myInteger = myInteger - 2048
        # mySensor = myInteger * 0.015625
    elif (value_type == "DEGREE"):
        mySensor = getEncoder(pkt)
        # myInteger = (struct.unpack("B", pkt[0])[0]) * multiple + struct.unpack("B", pkt[1])[0];
        # mySensor = (myInteger >> 1) & 0x3FFF
        # mySensor = myInteger
    return mySensor


def getAcc(pkt):
    # myInteger = (struct.unpack("B", pkt[0])[0] & 0x07) * 256 + struct.unpack("B", pkt[1])[0];  #16G
    myInteger = struct.unpack("B", pkt[0])[0];
    if (myInteger > 127):
        myInteger = myInteger - 256
    acc = myInteger * 0.015625
    return acc


def getEncoder(pkt):
    myInteger = (struct.unpack("B", pkt[1])[0] & 0x0f) * 256 + struct.unpack("B", pkt[0])[0];
    myInteger = myInteger >> 1
    encoder = myInteger * 360 / 1023
    return encoder


def getString(pkt):
    myString = ""
    for c in pkt:
        myString += "%02x" % struct.unpack("B", c)[0]
        # myString += c[0]
    return myString


def getACIItoString(pkt):
    myString = "";
    for c in pkt:
        myString += "%s" % chr(struct.unpack("B", c)[0])
    return myString


def getBCD(c):
    myString = "";
    myString = "%x" % (struct.unpack("B", c)[0] >> 4 & 0x0F) + "." + "%x" % (struct.unpack("B", c)[0] & 0x0F) + "V"
    return myString


def getRSSI(c):
    return struct.unpack("b", c)[0]


def getDegree(f1, f2, f3, cal_pitch, accx):
    degree = atan2(f1, sqrt(pow(f2, 2) + pow(f3, 2))) * 180 / pi - cal_pitch
    if (accx < 0):
        if (degree > 0):
            degree = 180 - degree
        else:
            degree = -180 - degree
    return degree


def getPitch(accx, accy, accz, cal_pitch):
    pitch = atan(accz/(sqrt(pow(accx,2) + pow(accy,2)))) *180/pi
    if accx < 0:
        if accz > 0:
            pitch = 180 - pitch
        else:
            pitch = -180 - pitch
    return pitch - cal_pitch

def getRoll(accx, accy, accz, cal_roll):
    roll = atan(accy/(sqrt(pow(accx,2) + pow(accz,2)))) *180/pi
    return roll - cal_roll

def getAccSum(accx, accy, accz):
    return sqrt(pow(accx,2) + pow(accy,2) + pow(accz,2))
