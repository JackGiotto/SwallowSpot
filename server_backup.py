
# process running in the backup server for Swallow Spot DB

import socket
import ssl

host = '0.0.0.0'
port = 12345

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # crea un socket TCP

server_sock.bind((host, port))                                      # lega socket con IP e porta

server_sock.listen()                                                # socket in ascolto

print(f"In attesa di connessioni su {host}:{port}...")              

client_sock, addr = server_sock.accept()                            # socket accetta la connessione

ssl_client_sock = ssl.wrap_socket(client_sock, server_side=True, certfile="certificate/server.pem", keyfile="certificate/server.key")     # Abilita la crittografia SSL/TLS

print(f"Connessione da {addr} stabilita.")

# Ricevi e invia dati attraverso il socket crittografato
data = ssl_client_sock.recv(1024)
print(f"Received: {data.decode()}")

ssl_client_sock.send(b"Hello, client!")

# Chiudi il socket crittografato
ssl_client_sock.close()

# Chiudi il socket del server
server_sock.close()

# per creare certificato: openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.pem
