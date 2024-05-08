
# process running in the server for Swallow Spot DB
import socket, ssl, subprocess

"""
# Define the command and arguments
command = ['mysqldump', '-u', 'martini', '-p' 'martinid78', 'Swallow Spot']

# Execute the command using subprocess.Popen
try:
    # Open the process with stdin=subprocess.PIPE to allow providing the password
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Read the output
    output, error = process.communicate()

    if process.returncode == 0:
        with open('backup.sql', 'w') as backup_file:
            backup_file.write(output)
        print("Database backup created successfully.")
    else:
        print("Error occurred while creating database backup:", error)
except Exception as e:
    print("Error:", e)
"""

import socket, ssl

ipAddr = '127.0.0.1'
port = 8495

with open('new_backup.sql', 'rb') as f:
    backup_data = f.read()

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH) # Create an SSL context

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_client_socket = context.wrap_socket(client_socket, server_hostname="localhost")

ssl_client_socket.connect((ipAddr, port))

ssl_client_socket.send(backup_data)

message = ssl_client_socket.recv(1024)

if message.decode() == str(len(backup_data)):
    print('Backup completed successfully!')

ssl_client_socket.close()

