#!usr/bin/python

import pymysql
from isensit_gw import ISensitGW
import datetime

class ISensitGWMysql(object):
    def __init__(self):
        self.config_data = ISensitGW()
        self.config_data.init_json_config_data()
        self.table = self.config_data.get_mysql_credentials()['acc_beacon_table']
#	self.table = "smulder"
        self.connection = None
        self.gatewayID = self.config_data.get_gateway_name()
        self.sleeptime = self.config_data.get_mysql_sleeptime()
    	self.start_time = self.config_data.get_start_time()
	self.end_time = self.config_data.get_end_time()

    def connect_to_db(self):
        try:
            self.connection = pymysql.connect(
                host=self.config_data.get_mysql_credentials()['hostname'],
                user=self.config_data.get_mysql_credentials()['username'],
                password=self.config_data.get_mysql_credentials()['password'],
                db=self.config_data.get_mysql_credentials()['database'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

        except pymysql.Error as e:
            print("Connection error: ", str(e))
            return False

        except Exception as e:
            print("Mysql error: ", str(e))
            return False

        else:
            return self.connection

    def close_db(self):
        if self.connection.open:
            self.connection.close()

    def get_cursor(self):
        if self.connection.open:
            return self.connection.cursor()

    # def set_table(self, table):
    #     self.table = self.config_data.get_mysql_credentials()[table]
    #
    # def get_first_row_id(self):
    #     return 0


    def read_first_data(self, table_name):
        self.table = self.config_data.get_mysql_credentials()[table_name]
	try:
            with self.connection.cursor() as cursor:
                # Create a new record
                cursor.execute("SELECT * from " + self.table + " limit 1;")

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
#		print "cursor ", cursor.rowcount
                return cursor.fetchone()
            else:
                return None


    def __sizeof__(self):
        return super().__sizeof__()


    def insert_acc_beacon_data(self, beacon_id, beacon_accx, beacon_accy, beacon_accz, beacon_rssi, bad_lift, total_lift, state, currenttime, small_count, middle_count, large_count):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO " + self.table + " VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (beacon_id, beacon_accx, beacon_accy, beacon_accz, beacon_rssi, currenttime, bad_lift, total_lift, state, small_count, middle_count, large_count))

        except Exception as e:
            print("Error :", str(e))
            self.connection.rollback()
            return False

        else:
	    self.connection.commit()

    def read_acc_beacon_data(self, table_name):
	self.table = self.config_data.get_mysql_credentials()[table_name]
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                cursor.execute("SELECT * from " + self.table + " limit 1;")

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchone()
            else:
                return None
                
    def delete_data(self, table_name, row_count):
        cursor = self.connection.cursor()
        self.table = self.config_data.get_mysql_credentials()[table_name]
        delete_stmt = "DELETE FROM " + self.table + " WHERE row_count = %s"
#	print delete_stmt, "  ", row_count
        cursor.execute(delete_stmt, (row_count,))
	cursor.close()
        self.connection.commit()

    def delete_acc_beacon_data(self, table_name, beacon_id, row_count):
        cursor = self.connection.cursor()
        self.table = self.config_data.get_mysql_credentials()[table_name]
        delete_stmt = "DELETE FROM " + self.table + " WHERE beacon_id = %s AND row_count < %s"
#       print delete_stmt, "  ", row_count
        cursor.execute(delete_stmt, (beacon_id, row_count,))
	cursor.close()
        self.connection.commit()

        
    def read_last_acc_beacon_data(self, table_name, beacon_id):
	self.table = self.config_data.get_mysql_credentials()[table_name]
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
				sql = "SELECT * from " + self.table + " WHERE beacon_id = %s order by row_count desc limit 1;"
				cursor.execute(sql, beacon_id)

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchone()
            else:
                return None

    def read_distinct_acc_beacon_data(self):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "SELECT DISTINCT(beacon_id) from acc_beacons;"
                cursor.execute(sql)

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchall()
            else:
                return None


    def get_data_count(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM " + self.table)
        return cursor.rowcount


    def read_user_data(self, row_count):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from " + self.table + " where user_id = %s", row_count)
        return cursor.fetchone()

    def delete_user_data(self, row_count):
        cursor = self.connection.cursor()
        delete_stmt = "DELETE FROM " + self.table + " WHERE user_id %s"
        cursor.execute(delete_stmt, (row_count,))
	cursor.close()
        self.connection.commit()
        
    def insert_noise_data(self, noise_id, sensor_db):
        self.table = self.config_data.get_mysql_credentials()['noise_sensor_table']
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO " + self.table + " VALUES (NULL, %s, %s, CURRENT_TIMESTAMP)"
                cursor.execute(sql, (noise_id, sensor_db))

        except Exception as e:
            print("Error :", str(e))
            self.connection.rollback()
            return False

        else:
            self.connection.commit()



    def insert_fd_data(self, fd_id, pm, temp, hum, pm_hour):
        self.table = self.config_data.get_mysql_credentials()['fd_sensor_table']
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO " + self.table + " VALUES (NULL, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)"
                cursor.execute(sql, (fd_id, pm, temp, hum, pm_hour))

        except Exception as e:
            print("Error :", str(e))
            self.connection.rollback()
            return False

        else:
            self.connection.commit()

    def insert_acc_pitch_roll_data(self, beacon_id, beacon_accx, beacon_accy, beacon_accz, beacon_rssi, currenttime, beacon_accsum, pitch, roll, levelPitch, levelRoll, pitchList, rollList, teller, num):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO " + self.table + " VALUES (NULL, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(sql, (beacon_id, beacon_accx, beacon_accy, beacon_accz, beacon_rssi, beacon_accsum, pitch, roll, levelPitch, levelRoll, pitchList[0], pitchList[1], pitchList[2], pitchList[3], rollList[0], rollList[1], rollList[2], rollList[3], rollList[4], teller, num,))
        except Exception as e:
            print("Error :", str(e))
            self.connection.rollback()
            return False

        else:
            self.connection.commit()

    def insert_rssi_data(self, beacon_id, rssi_avr, created_at):
        self.table = self.config_data.get_mysql_credentials()['noise_sensor_table']
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO rssi VALUES (NULL, %s, %s, %s)"
                cursor.execute(sql, (beacon_id, rssi_avr, created_at))

        except Exception as e:
            print("Error :", str(e))
            self.connection.rollback()
            return False

        else:
            self.connection.commit()


    def read_cal_val(self, beacon_id):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                                sql = "SELECT * from users WHERE beacon_id = %s"
                                cursor.execute(sql, (beacon_id))

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchone()
            else:
                return None


    def read_all_data(self, table_name):
        self.table = self.config_data.get_mysql_credentials()[table_name]
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                cursor.execute("SELECT * from " + self.table)

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchall()
            else:
                return None
        
    def read_earliest_acc_beacon_data(self, beacon_id):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                                sql = "SELECT created_at from acc_beacons WHERE beacon_id = %s ORDER BY created_at asc limit 1"
                                cursor.execute(sql, (beacon_id))

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchone()
            else:
                return None

    def read_earliest_acc_beacon_datas(self, beacon_id, created_at):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                                sql = "SELECT beacon_rssi from acc_beacons WHERE beacon_id = %s and created_at = %s"
                                cursor.execute(sql, (beacon_id, created_at))

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchall()
            else:
                return None

    def read_next_acc_beacon_data(self, beacon_id, created_at):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                cursor.execute("SELECT * from acc_beacons where beacon_id = %s and created_at > %s limit 1", (beacon_id, created_at))

        except Exception as e:
            print("Error :", str(e))
            return None

        else:
            if cursor.rowcount > 0:
                return cursor.fetchall()
            else:
                return None

    def delete_earliest_beacon_data(self, beacon_id, created_at):
        cursor = self.connection.cursor()
        delete_stmt = "DELETE FROM acc_beacons WHERE beacon_id = %s and created_at = %s"
#       print delete_stmt, "  ", row_count
        cursor.execute(delete_stmt, (beacon_id, created_at,))
        self.connection.commit()


    def isConnected(self):
	return self.connection

    def half_hour(self):
    	currenttime = datetime.datetime.now()
    	return currenttime.minute == 00 or currenttime.minute == 30


    def working(self):
    	currenttime = datetime.datetime.now()
    	currentdate = currenttime.strftime("%Y-%m-%d")
    	start_t = datetime.datetime.strptime(currentdate + self.start_time, "%Y-%m-%d %H:%M:%S")
    	end_t = datetime.datetime.strptime(currentdate + self.end_time, "%Y-%m-%d %H:%M:%S")
    	today = currenttime.weekday()
        return currenttime > start_t and currenttime < end_t and today < 5

