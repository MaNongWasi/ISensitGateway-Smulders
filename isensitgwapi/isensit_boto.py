from __future__ import print_function # Python 2/3 compatibility
import boto3
import time
from boto3.dynamodb.conditions import Key, Attr
import csv, json, sys, decimal, logging

