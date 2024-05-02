
# process running in the backup server for Swallow Spot DB

import socket
import ssl

# Create an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="certificate/server.crt", keyfile="certificate/server.key")

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a host and port
server_socket.bind(('0.0.0.0', 8080))

# Listen for incoming connections
server_socket.listen(5)

print("Server is listening...")

while True:
    # Accept incoming connection
    client_socket, addr = server_socket.accept()
    
    # Wrap the socket with SSL
    ssl_client_socket = context.wrap_socket(client_socket, server_side=True)
    
    # Handle incoming data
    data = ssl_client_socket.recv(1024)
    if data:
        print("Received:", data.decode())
        ssl_client_socket.send("Hello from server!".encode())
    
    # Close the connection
    ssl_client_socket.close()

# per creare certificato: openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.pem
