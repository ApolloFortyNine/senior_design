import socket
import json
import sqlite3
import logging
import time
from logging.handlers import TimedRotatingFileHandler

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(filename='sock.log', when='D', interval=1)
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(log_formatter)
logger.addHandler(handler)


# Send 1 json object containing first 10 keys, then another with the rest in another packet
def main():
    # Socket creation
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 5001
    server_socket.bind((socket.gethostname(), port))
    server_socket.listen(5)
    logger.info("Successfully started listening on port {0}".format(port))
    data_dict_1 = {}
    data_dict_2 = {}
    filled_time = 0
    # TODO: Wrap everything in a try catch, so it doesn't crash when an improper resquest is sent
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
                if not data_dict_1 or ((time.time() - filled_time) >= 5):
                    data_dict_1 = json.loads(test_str)
                    filled_time = time.time()
                    logger.info("Filled first data_dict")
                    continue
                data_dict_2 = json.loads(test_str)
                logger.info("Filled second data_dict")
                data_dict_2.update(data_dict_1)
                logger.info("Received valid data, sending to database")
                fill_db(data_dict_2)
                data_dict_1 = {}
                data_dict_2 = {}
            client.close()
        except:
            logger.exception("Invalid data caused exception:")
            data_dict_1 = {}
            data_dict_2 = {}
            client.close()


def fill_db(data_dict):
    conn = sqlite3.connect('glove.db3')
    c = conn.cursor()

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
