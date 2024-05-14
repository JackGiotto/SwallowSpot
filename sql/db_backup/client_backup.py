
# process running in the Swallow Spot DB server

import socket, ssl, subprocess          # libraries 

command = ['mysqldump', '-u', 'martini', '-p' 'martinid78', 'Swallow Spot']         # arguments of the command

try:        # errors management
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)  # Open the process with stdin=subprocess.PIPE to allow providing the password

    output, error = process.communicate()   # Read the output

    if process.returncode == 0:
        with open('backup.sql', 'w') as backup_file:
            backup_file.write(output)
        print("Database backup created successfully.")
    else:
        print("Error occurred while creating database backup:", error)

except Exception as e:
    print("Error:", e)

ipAddr = '146.247.68.35'        # address of the server to connect
port = 8495                     # port of the socket to connect

with open('backup.sql', 'rb') as f:     # opens the backup file reading it as bytes
    backup_data = f.read()              # writes the contents as bytes into the variable

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)       # Creates an SSL context

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   

ssl_client_socket = context.wrap_socket(client_socket, server_hostname="localhost")

ssl_client_socket.connect((ipAddr, port))

ssl_client_socket.send(backup_data)             # sends the backup data in bytes to the server socket

message = ssl_client_socket.recv(1024)          # receives the message from the server with the size of the data received

if message.decode() == str(len(backup_data)):       # controls if the size of the message and the size of the backup are the same
    print('Backup completed successfully')
else:
    print('Backup wasn''t completed successfully: some informations miss')

ssl_client_socket.close()                   # closes the connection with the socket

