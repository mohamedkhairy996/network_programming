
"""
@author: mohamed khairy
"""


from socket import *
import threading as th

chat = socket(AF_INET, SOCK_STREAM)
server_ip = '127.0.0.1'
server_port = 7000

chat.connect((server_ip, server_port))
while True:
    x = input('Client : ')
    if x == 'q':
        print('connection closed')
        chat.send(x.encode('utf-8'))
        break

    # Send the length of the message (fixed size: 10 bytes)
    message_data = x.encode('utf-8')
    message_length = str(len(message_data)).zfill(10).encode('utf-8')
    chat.send(message_length)

    # Send the actual message
    chat.send(message_data)

    # Receive the length of the message (fixed size: 10 bytes)
    length_data = chat.recv(10)
    length = int(length_data.decode('utf-8'))

    # Receive the message with variable length
    received_message = chat.recv(length).decode('utf-8')
    print("Server : " + received_message)

chat.close()
