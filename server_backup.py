
# process running in the backup server for Swallow Spot DB

import socket, ssl

listen = True
ipAddr = '0.0.0.0'
port = 8495

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH) # SSL context
context.load_cert_chain(certfile="certificate/server.crt", keyfile="certificate/server.key") # Load server certificate

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((ipAddr, port))

server_socket.listen(5)

while listen == True:
    try:
        print("Server is listening...")
        client_socket, addr = server_socket.accept()

        ssl_client_socket = context.wrap_socket(client_socket, server_side=True)

        backup_data = b''
        while True:
            chunk = ssl_client_socket.recv(1024)
            backup_data += chunk

            if len(chunk) < 1024:
                break

        filename = "backup.sql"
        with open(filename, 'wb') as f:
            f.write(backup_data)

        message = str(len(backup_data))
        ssl_client_socket.send(message.encode())
        ssl_client_socket.close()

        print("Socket client has been closed...")
    except KeyboardInterrupt:
        print('Server chiuso')
        listen = False

        
    