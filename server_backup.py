
# process running in the backup server for Swallow Spot DB

import socket, ssl

listen = True
ipAddr = '0.0.0.0'
port = 8495

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)                                               # contesto SSL
context.load_cert_chain(certfile="certificate/server.crt", keyfile="certificate/server.key")    # caricamento dei certificati

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # create an Internet Socket for TCP Connection

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((ipAddr, port))      # Bind the socket to a host and port

server_socket.listen(5)     # socket in ascolto

while listen == True:

    try:
        print("Server is listening...")
        
        client_socket, addr = server_socket.accept()                    # accetta le connessioni in arrivo
        
        ssl_client_socket = context.wrap_socket(client_socket, server_side=True)    # aggiunge protocollo SSL al socket
        
        backup_data = b''
        
        while True:
            chunk = ssl_client_socket.recv(1024)
            backup_data += chunk
            
            if chunk < bytes(1024):
                break
        
        filename = "backup.sql"

        with open(filename, 'wb') as f:
            f.write(backup_data)

        message = 'Finished successfully'
        server_socket.send(message.encode())                                      # chiude la connessione
        
        print("Socket client has been closed...")

    except KeyboardInterrupt:
        print('Server chiuso')
        listen = False
        
    