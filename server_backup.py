"""
import ssl
import socket

BUFF_SIZE = 1024

if __name__ == "__main__":
    # First, create a context. The default settings are probably the best here. 
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # Load the CA (self-signed, in this case) and the corresponding private key (also self-signed, in this case)
    context.load_cert_chain(certfile="certificate/server.crt", keyfile="certificate/server.key")

    # Create a standard TCP socket, bind it to an address, and listen for connections
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 8080))
    s.listen()

    # Start accepting incoming connections
    accepting = True 
    try:
        while accepting:
            # conn is a standard python socket, addr is where it originated
            conn, addr = s.accept()
            # wrap the standard socket with the SSLContext, now it is a secure connection
            with context.wrap_socket(conn, server_side=True) as secure_conn:
                # data can be read/sent just like as in standard sockets
                data = secure_conn.recv(BUFF_SIZE)
                print(data)
    except socket.timeout:
        pass
"""
    
# process running in the backup server for Swallow Spot DB

import socket
import ssl

listen = True
ipAddr = '0.0.0.0'
port = 8085

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
        
        # Receive the file data
        backup_data = b''
        while True:
            chunk = ssl_client_socket.recv(1024)
            if chunk < bytes(1024):
                break
            backup_data += chunk
            
        if backup_data:
            filename = "new_backup.sql"

            # Write the file data to a new file
            with open(filename, 'wb') as f:
                f.write(backup_data)
                                       # stampa il messaggio
            # ssl_client_socket.send("Thanks for the file!".encode())       # invia un messaggio crittato al client
        
        ssl_client_socket.close()                                       # chiude la connessione
        
    except KeyboardInterrupt:
        print('Server chiuso')
        listen = False