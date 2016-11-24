#!/bin/bash

#path defines
working_dir=/home/pi/ISensitGateway
module_dir=isensitgw_ble_reader
module=isensitgw_ble_reader.pyc
error_file=isensitgw.error
error_path=$working_dir/$error_file
status_file=$working_dir/$module_dir/$module_dir.status

# Define a timestamp function
timestamp() {
	date "+%Y-%m-%d %H:%M:%S"
}

scriptname=`basename "$0"`
filename=$working_dir/$module_dir/$module

until python $filename > $status_file; do
   echo `timestamp` "Process $filename crashed with exit code $?.  Respawning." >&2
done

echo "`timestamp` : $scriptname, this script failed " >> $error_path 2>&1
echo "`timestamp` : $filename exited with a status of : " $? >> $error_path 2>&1



