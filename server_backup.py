
# process running in the backup server for Swallow Spot DB

import socket, ssl

listen = True
ipAddr = '0.0.0.0'
port = 8492

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)                                               # contesto SSL
context.load_cert_chain(certfile="certificate/server.crt", keyfile="certificate/server.key")    # caricamento dei certificati

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # create an Internet Socket for TCP Connection

server_socket.bind((ipAddr, port))      # Bind the socket to a host and port

server_socket.listen(5)     # socket in ascolto

print("Server is listening...")

while listen == True:

    try:
        
        client_socket, addr = server_socket.accept()                    # accetta le connessioni in arrivo
        
        ssl_client_socket = context.wrap_socket(client_socket, server_side=True)    # aggiunge protocollo SSL al socket
        
        backup_data = b''
        
        while True:
            chunk = ssl_client_socket.recv(1024)
            backup_data += chunk
            
            if chunk < bytes(1024):
                break
        
        filename = "new_backup.sql"

        with open(filename, 'wb') as f:
            f.write(backup_data)

        ssl_client_socket.close()                                       # chiude la connessione
        
    except KeyboardInterrupt:
        print('Server chiuso')
        listen = False
        
    