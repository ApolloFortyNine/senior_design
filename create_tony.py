import sqlite3

conn = sqlite3.connect('tony.db3')
c = conn.cursor()
schema = """CREATE TABLE `Data` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`unix_timestamp`	NUMERIC,
	`letter`	TEXT,
	`thumb_flex`	NUMERIC,
	`index_flex`	NUMERIC,
	`middle_flex`	NUMERIC,
	`ring_flex`	NUMERIC,
	`pinky_flex`	NUMERIC,
	`thumb_cap`	INTEGER,
	`index_cap_upper`	INTEGER,
	`index_cap_lower`	INTEGER,
	`index_cap_other`	INTEGER,
	`middle_cap_upper`	INTEGER,
	`middle_cap_lower`	INTEGER,
	`ring_cap_upper`	INTEGER,
	`ring_cap_lower`	INTEGER,
	`pinky_cap_upper`	INTEGER,
	`pinky_cap_lower`	INTEGER,
	`imu_acc_x`	NUMERIC,
	`imu_acc_y`	NUMERIC,
	`imu_acc_z`	NUMERIC,
	`imu_gyro_x`	NUMERIC,
	`imu_gyro_y`	NUMERIC,
	`imu_gyro_z`	NUMERIC
);"""
c.execute(schema)
conn.close()
