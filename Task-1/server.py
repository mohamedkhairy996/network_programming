# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:00:16 2024

@author: moham
"""

from socket import *
import threading as th

server = socket(AF_INET, SOCK_STREAM)
server_ip = '127.0.0.1'
server_port = 7000

server.bind((server_ip, server_port))
server.listen()

print("Server is listening...")

def handle_client(client_socket):
    while True:
        try:
            client_message = client_socket.recv(2048).decode('UTF-8')
            if not client_message:
                break
            print('Client message:', client_message)
            if client_message == 'close':
                break
        except ConnectionResetError:
            print("Connection closed by client.")
            break

    client_socket.close()

while True:
    client_socket, addr = server.accept()
    print(f"Connection from {addr} has been established.")
    client_handler = th.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()

input()