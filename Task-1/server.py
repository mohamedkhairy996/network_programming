
"""
@author: mohamed khairy
"""

from socket import *


server = socket(AF_INET, SOCK_STREAM)
server_ip = '127.0.0.1'
server_port = 7000

server.bind((server_ip, server_port))
server.listen()

print("Server is listening...")

client_socket, addr = server.accept()
print(f"Connection from {addr} has been established.")

while True:
    # Receiving the length of the message 
    length_data = client_socket.recv(10)
    length = int(length_data.decode('utf-8'))

    # Receiving the message with variable length
    received_message = client_socket.recv(length).decode('utf-8')
    print("Client: " + received_message)

    # Prompting the server for a response
    server_response = input('Server: ')

    # Checking if the server wants to quit
    if server_response == 'q':
        print('connection closed')
        client_socket.close()
        break

    # Sending the length of the message (fixed size: 10 bytes)
    message_data = server_response.encode('utf-8')
    message_length = str(len(message_data)).zfill(10).encode('utf-8')
    client_socket.send(message_length)

    # Sending the actual message
    client_socket.send(message_data)

client_socket.close()
