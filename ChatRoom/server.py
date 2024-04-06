import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 7000

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = {}
addresses = {}

# Handling Messages From Clients
def handle(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message == 'quit':
                    client_socket.close()
                    del clients[client_socket]
                    break
                elif message.startswith('@'):
                    recipient_name, content = message.split(':',1)
                    recipient_found = False
                    
                    for sock, name in clients.items():
                        if name == recipient_name[1:]:
                            recipient_found = True
                            recipient_socket = sock
                            recipient_socket.send(f"Message from {clients[client_socket]}: {content}".encode('utf-8'))
                            break
                    if not recipient_found:
                        client_socket.send(f"User '{recipient_name[1:]}' not found.".encode('utf-8'))
                else:
                    client_socket.send("Invalid command. Use '@username:message' to send a private message.".encode('utf-8'))
        except:
            print(f"Connection with {addresses[client_socket]} terminated.")
            client_socket.close()
            del clients[client_socket]
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client_socket, client_address = server.accept()
        print(f"Connected with {client_address}")

        # Request And Store Nickname
        client_socket.send('NICK'.encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = nickname
        addresses[client_socket] = client_address
        
        # Print And Broadcast Nickname
        print(f"Nickname is {nickname}")
        client_socket.send('Connected to server!'.encode('utf-8'))
        
       
        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client_socket, client_address))
        thread.start()

receive()
