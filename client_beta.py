# client code
import socket
import random

DATA_SIZE = 65536
IP = '25.42.252.196'
actual_port = 9091


# sock_client = socket.socket()


def connect_server():
    global sock_client
    sock_client = socket.socket()
    sock_client.settimeout(5)
    sock_client.connect((IP, actual_port))


def game_coord_client():
    pass


def send_gd_to_server(game_data):
    sock_client.send(game_data.encode())


def send_data_to_server(data):
    sock_client.send(data.encode())


def recv_data_from_server():
    return sock_client.recv(DATA_SIZE).decode()


def close_connection():
    sock_client.close()


if __name__ == 'main':
    close_connection()
