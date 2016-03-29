import socket
import time

send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.connect((socket.gethostname(), 5001))
# send_socket.send(bytes('{"t_f": 1.5062, "i_f": 1.7029, "m_f": 1.2012, "r_f": 1.809, "p_f": 1.221, "t_c": 1, "i_cu": 0, "i_cl": 0, "i_co": 1, "m_cu": 0, "m_cl": 0, "r_cu": 0, "r_cl": 0, "p_cu": 0, "p_cl": 0, "imu_ax": 0.1235, "imu_ay": 0.354, "imu_az": 0.561, "imu_gx": 0.0123, "imu_gy": 0.365, "imu_gz": 0.891}', 'utf-8'))
send_socket.send(bytes('{"t_f": 1.5062, "i_f": 1.7029, "m_f": 1.2012, "r_f": 1.809, "p_f": 1.221, "t_c": 1, "i_cu": 0, "i_cl": 0, "i_co": 1, "m_cu": 0, "m_cl": 0, "r_cu": 0, "r_cl": 0, "p_cu": 0, "p_cl": 0, "imu_ax": 0.1235, "imu_ay": 0.354, "imu_az": 0.561, "imu_gx": 0.0123, "imu_gy": 0.365}', 'utf-8'))
send_socket.close()
time.sleep(4)
send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.connect((socket.gethostname(), 5001))
send_socket.send(bytes('{"imu_gz": 0.891}', 'utf-8'))
