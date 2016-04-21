from flask import Flask, jsonify, request
import sqlite3
app = Flask(__name__)

@app.route("/tony", methods=['GET', 'POST'])
def tony():
    if request.headers['Content-Type'] == 'application/json':
        conn = sqlite3.connect('tony.db3')
        c = conn.cursor()
        c.execute("SELECT * FROM Data")
        tony_data = c.fetchone()
        # return str(tony_data)
        tony_dict = {}
        tony_dict['unix_timestamp'] = tony_data[1]
        tony_dict['letter'] = tony_data[2]
        tony_dict['thumb_flex'] = tony_data[3]
        tony_dict['index_flex'] = tony_data[4]
        tony_dict['middle_flex'] = tony_data[5]
        tony_dict['ring_flex'] = tony_data[6]
        tony_dict['pinky_flex'] = tony_data[7]
        tony_dict['imu_acc_x'] = tony_data[18]
        tony_dict['imu_acc_y'] = tony_data[19]
        tony_dict['imu_acc_z'] = tony_data[20]
        return jsonify(**tony_dict)
    conn = sqlite3.connect('tony.db3')
    c = conn.cursor()
    c.execute("SELECT * FROM Data")
    tony_data = c.fetchone()
    # return str(tony_data)
    tony_dict = {}
    tony_dict['unix_timestamp'] = tony_data[1]
    tony_dict['letter'] = tony_data[2]
    tony_dict['thumb_flex'] = tony_data[3]
    tony_dict['index_flex'] = tony_data[4]
    tony_dict['middle_flex'] = tony_data[5]
    tony_dict['ring_flex'] = tony_data[6]
    tony_dict['pinky_flex'] = tony_data[7]
    tony_dict['imu_acc_x'] = tony_data[18]
    tony_dict['imu_acc_y'] = tony_data[19]
    tony_dict['imu_acc_z'] = tony_data[20]
    return jsonify(**tony_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
