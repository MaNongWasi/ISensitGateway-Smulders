#!/bin/bash


echo "This is the Launcher for ISensit Gateway"
echo `date` > /var/log/ISensitGW.log 2>&1
sudo /usr/bin/python /home/pi/Desktop/Jingjing/Deployment/Main.py >> /var/log/ISensitGW.log 2>&1 &


