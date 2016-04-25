import socket
import json
import sqlite3
import logging
import time
from sklearn import tree
from sklearn import datasets, svm, metrics
import sqlite3
from logging.handlers import TimedRotatingFileHandler

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(filename='sock.log', when='D', interval=1)
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(log_formatter)
logger.addHandler(handler)
last_letter = ""


def main():
    conn = sqlite3.connect('glove.db3')
    c = conn.cursor()

    c.execute("""SELECT * FROM Data""")
    results = c.fetchall()
    data_arr = []
    target_arr = []
    for x in results:
        data_arr.append(list(x[3:]))
        target_arr.append(x[2])
    # print(data_arr)
    svm1 = svm.SVC(gamma=0.01, C=4.65)
    svm1.fit(data_arr, target_arr)
    svm2 = svm.SVC(gamma=0.2)
    svm2.fit(data_arr, target_arr)
    svm3 = svm.SVC(gamma=0.05)
    svm3.fit(data_arr, target_arr)
    clf1 = tree.DecisionTreeClassifier()
    clf1.fit(data_arr, target_arr)
    # Socket creation
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 5001
    server_socket.bind((socket.gethostname(), port))
    server_socket.listen(5)
    logger.info("Successfully started listening on port {0}".format(port))
    while True:
        try:
            client, address = server_socket.accept()
            data = client.recv(1024)
            if data:
                test_str = str(data, 'utf-8')
                if test_str[0] != '{' or test_str[-1] != '}':
                    logger.warning("Received invalid data: {0}".format(test_str))
                    client.close()
                    continue
                logger.debug("Received data: {0}".format(test_str))
                data_dict = json.loads(test_str)
                logger.info("Received valid data, sending to predicter")
                predict_letter(data_dict, clf1, svm1, svm2, svm3)
            client.close()
        except:
            logger.exception("Invalid data caused exception:")
            client.close()


def predict_letter(data_dict, clf, svm1, svm2, svm3):
    data = data_dict['data']
    #prediction = clf.predict(data)[0]
    prediction = svm1.predict(data)[0]
    global last_letter
    if (prediction != last_letter):
        last_letter = prediction
        return
    print("Tree: " + clf.predict(data)[0])
    print("SVM G .01 C 4.65: " + str(svm1.predict(data)))
    print("SVM .2: " + str(svm2.predict(data)))
    print("SVM .05: " + str(svm3.predict(data)))
    print(data_dict)
    conn = sqlite3.connect('tony.db3')
    c = conn.cursor()
    c.execute("DELETE FROM Data;")
    conn.commit()
    data_dict['t_f'] = data[0]
    data_dict['i_f'] = data[1]
    data_dict['m_f'] = data[2]
    data_dict['r_f'] = data[3]
    data_dict['p_f'] = data[4]
    data_dict['t_c'] = data[5]
    data_dict['i_cu'] = data[6]
    data_dict['i_cl'] = data[7]
    data_dict['i_co'] = data[8]
    data_dict['m_cu'] = data[9]
    data_dict['m_cl'] = data[10]
    data_dict['r_cu'] = data[11]
    data_dict['r_cl'] = data[12]
    data_dict['p_cu'] = data[13]
    data_dict['p_cl'] = data[14]
    data_dict['imu_ax'] = data[15]
    data_dict['imu_ay'] = data[16]
    data_dict['imu_az'] = data[17]
    data_dict['imu_gx'] = data[18]
    data_dict['imu_gy'] = data[19]
    data_dict['imu_gz'] = data[20]
    c.execute("""INSERT INTO Data (unix_timestamp, thumb_flex, index_flex, middle_flex, ring_flex, pinky_flex, thumb_cap,
                 index_cap_upper, index_cap_lower, index_cap_other, middle_cap_upper, middle_cap_lower,
                 ring_cap_upper, ring_cap_lower, pinky_cap_upper, pinky_cap_lower, imu_acc_x, imu_acc_y,
                 imu_acc_z, imu_gyro_x, imu_gyro_y, imu_gyro_z, letter)
                 VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13},
                 {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}, '{22}')""".format(time.time(),
                                                                           data_dict['t_f'],
                                                                           data_dict['i_f'],
                                                                           data_dict['m_f'],
                                                                           data_dict['r_f'],
                                                                           data_dict['p_f'],
                                                                           data_dict['t_c'],
                                                                           data_dict['i_cu'],
                                                                           data_dict['i_cl'],
                                                                           data_dict['i_co'],
                                                                           data_dict['m_cu'],
                                                                           data_dict['m_cl'],
                                                                           data_dict['r_cu'],
                                                                           data_dict['r_cl'],
                                                                           data_dict['p_cu'],
                                                                           data_dict['p_cl'],
                                                                           data_dict['imu_ax'],
                                                                           data_dict['imu_ay'],
                                                                           data_dict['imu_az'],
                                                                           data_dict['imu_gx'],
                                                                           data_dict['imu_gy'],
                                                                           data_dict['imu_gz'],
                                                                           prediction))

    conn.commit()
    conn.close()


def fill_db(data_dict_in):
    conn = sqlite3.connect('glove.db3')
    c = conn.cursor()
    data_dict = {}
    data = data_dict_in['data']
    # Order:
    # t_c, i_cu, i_cl, i_co, m_cu, m_cl, r_cu, r_cl, p_cu,
    # p_cl, t_f, i_f, m_f, r_f, p_f, imu_gx, imu_gy, imu_gz, imu_ax, imu_ay,
    # imu_az);
    data_dict['t_c'] = data[0]
    data_dict['i_cu'] = data[1]
    data_dict['i_cl'] = data[2]
    data_dict['i_co'] = data[3]
    data_dict['m_cu'] = data[4]
    data_dict['m_cl'] = data[5]
    data_dict['r_cu'] = data[6]
    data_dict['r_cl'] = data[7]
    data_dict['p_cu'] = data[8]
    data_dict['p_cl'] = data[9]
    data_dict['t_f'] = data[10]
    data_dict['i_f'] = data[11]
    data_dict['m_f'] = data[12]
    data_dict['r_f'] = data[13]
    data_dict['p_f'] = data[14]
    data_dict['imu_gx'] = data[15]
    data_dict['imu_gy'] = data[16]
    data_dict['imu_gz'] = data[17]
    data_dict['imu_ax'] = data[18]
    data_dict['imu_ay'] = data[19]
    data_dict['imu_az'] = data[20]
    c.execute("""INSERT INTO Data (unix_timestamp, thumb_flex, index_flex, middle_flex, ring_flex, pinky_flex, thumb_cap,
                 index_cap_upper, index_cap_lower, index_cap_other, middle_cap_upper, middle_cap_lower,
                 ring_cap_upper, ring_cap_lower, pinky_cap_upper, pinky_cap_lower, imu_acc_x, imu_acc_y,
                 imu_acc_z, imu_gyro_x, imu_gyro_y, imu_gyro_z)
                 VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13},
                 {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21})""".format(time.time(),
                                                                           data_dict['t_f'],
                                                                           data_dict['i_f'],
                                                                           data_dict['m_f'],
                                                                           data_dict['r_f'],
                                                                           data_dict['p_f'],
                                                                           data_dict['t_c'],
                                                                           data_dict['i_cu'],
                                                                           data_dict['i_cl'],
                                                                           data_dict['i_co'],
                                                                           data_dict['m_cu'],
                                                                           data_dict['m_cl'],
                                                                           data_dict['r_cu'],
                                                                           data_dict['r_cl'],
                                                                           data_dict['p_cu'],
                                                                           data_dict['p_cl'],
                                                                           data_dict['imu_ax'],
                                                                           data_dict['imu_ay'],
                                                                           data_dict['imu_az'],
                                                                           data_dict['imu_gx'],
                                                                           data_dict['imu_gy'],
                                                                           data_dict['imu_gz']))

    conn.commit()
    logger.info("Inserted data into sqlite database")
    conn.close()


def test_data():
    data = ('{"t_f": 1.5062, "i_f": 1.7029, "m_f": 1.2012, "r_f": 1.809, "p_f": 1.221, "t_c": 1, '
            '"i_cu": 0, "i_cl": 0, "i_co": 1, "m_cu": 0, "m_cl": 0, "r_cu": 0, "r_cl": 0, "p_cu": 0, '
            '"p_cl": 0, "imu_ax": 0.1235, "imu_ay": 0.354, "imu_az": 0.561, "imu_gx": 0.0123, '
            '"imu_gy": 0.365, "imu_gz": 0.891}')
    print(data)
    data_dict = json.loads(data)
    print(data_dict)
    fill_db(data_dict)

# Run the code
# test_data()
main()
