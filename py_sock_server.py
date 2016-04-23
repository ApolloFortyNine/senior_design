import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 5001))
server_socket.listen(5)
while True:
    client, address = server_socket.accept()
    data = client.recv(1024)
    if data:
        print(data)
    client.close()
