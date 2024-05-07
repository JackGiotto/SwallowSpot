
# process running in the server for Swallow Spot DB

import socket, ssl, subprocess

command = 'mysqldump -u martini -p "Swallow Spot" > backup.sql'
password = "password"

p = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
output, err = p.communicate(input=(password + '\n').encode())

print(output.decode())

ipAddr = '127.0.0.1'
port = 8085

with open('tables_creation.sql', 'rb') as f:     # Read the file content
    backup_data = f.read()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)   # Create an SSL context

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket

context.load_verify_locations("certificate/server.crt")     # caricato il certificato

ssl_client_socket = context.wrap_socket(client_socket, server_hostname="localhost")     

ssl_client_socket.connect((ipAddr, port))

ssl_client_socket.send(backup_data)     # invia il backup al server

ssl_client_socket.close()       # chiude il socket

# mysqldump -u martini -p "Swallow Spot" > backup.sql
