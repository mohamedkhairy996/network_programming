
"""
@author: mohamed khairy
"""


from socket import *
import threading as th

chat = socket(AF_INET, SOCK_STREAM)
server_ip = '127.0.0.1'
server_port = 7000

chat.connect((server_ip, server_port))

def receive(chat):
    while True:
        try:
            server_message = chat.recv(2048).decode('UTF-8')
            if not server_message:
                break
            print('Server message:', server_message)
        except ConnectionResetError:
            print("Connection closed by server.")
            break

receive_thread = th.Thread(target=receive, args=(chat,))
receive_thread.start()

while True:
    message = input('Send: ')
    if message == 'close':
        chat.send(message.encode('UTF-8'))
        break
    else:
        total_sent = 0
        message_bytes = message.encode('UTF-8')
        message_length = len(message_bytes)
        while total_sent < message_length:
            sent = chat.send(message_bytes[total_sent:])
            if sent == 0:
                print("Connection closed by server.")
                break
            total_sent += sent

chat.close()
