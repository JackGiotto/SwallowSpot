
# process running in the backup server for Swallow Spot DB

import socket, ssl          # libraries

ipAddr = '0.0.0.0'          # IP address to listen
port = 8495                 # port for the connection

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)                                   # SSL context
context.load_cert_chain(certfile="certificate/server.crt", keyfile="certificate/server.key")    # loads server certificate with the key

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # creates a TCP socket

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # allows the socket to reuse the port

server_socket.bind((ipAddr, port))      # bind the socket on the IP address and the port

server_socket.listen(5)                 # maximum number of simultaneous connection

while True:                     # endless loop

    print("Backup server is listening...")
    
    client_socket, addr = server_socket.accept()        # accepts the connection of the client socket
    print("Connection accepted with ", addr)
    
    ssl_client_socket = context.wrap_socket(client_socket, server_side=True)   

    backup_data = b''
    
    while True:
        chunk = ssl_client_socket.recv(1024)        # receives a slice of bytes
        backup_data += chunk                        # add the slice into the variable

        if len(chunk) < 1024:       # if the lenght of the size is 
            break

    filename = "new_backup.sql"
    with open(filename, 'wb') as f:
        f.write(backup_data)

    message = str(len(backup_data))
    ssl_client_socket.send(message.encode())
    ssl_client_socket.close()

    print("Connection has been closed")
    break

print('Server closed')      