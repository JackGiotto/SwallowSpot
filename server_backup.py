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
