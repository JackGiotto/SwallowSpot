# process running in the Swallow Spot DB server

import socket, ssl, subprocess          # libraries 
import os

def start_backup(IP_address:str , port_number:str) -> str:
    command = ['mysqldump', '-u', os.getenv("DBUSER"), '-p' + os.getenv("PASSWORD"), os.getenv('DBNAME')]         # arguments of the command

    try:        # errors management
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)      # Creates a sub-process to execute the command
        output, error = process.communicate()                                                               # Reads the output of the process
        print (error)

        if process.returncode == 0:                                                                 # if the operation was successfull
            with open('./utils/db_backup/backup/last_sended_backup.sql', 'w') as backup_file:       
                backup_file.write(output)
            print("Database backup created successfully.")
        else:
            print("Error occurred while creating database backup:", error)
            return "Errore: non mi sono riuscito a connettere"

    except Exception as e:
        print("Error:", e)
        return ("Errore generico")

    ipAddr = IP_address         # address of the server to connect
    port = int(port_number)     # port of the socket to connect

    print(ipAddr, port)

    with open('./utils/db_backup/backup/last_sended_backup.sql', 'rb') as f:        # opens the backup file reading it as bytes
        backup_data = f.read()                                                      # writes the contents as bytes into the variable

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)                           # SSL context creation
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                       # Socket creation
    ssl_client_socket = context.wrap_socket(client_socket, server_hostname="localhost")     # wraps the socket with SSL

    print((ipAddr, port))

    try:                                                # errors management
        ssl_client_socket.connect((ipAddr, port))       # encrypted connection with the socket
    except:         
        return "Errore di connessione"
    
    ssl_client_socket.send(backup_data)             # sends the backup data in bytes to the server socket

    message = ssl_client_socket.recv(1024)          # receives the message from the server with the size of the data received

    if message.decode() == str(len(backup_data)):                                   # controls if the size of the message and the size of the backup are the same
        print('Backup completed successfully')                                      # feedbacks of the operation
        result = "Success"
    else:
        print('Backup wasn''t completed successfully: some informations miss')      
        result = "Errore: il backup non è stato completato"

    ssl_client_socket.close()       # closes the connection with the socket
    return result                   # returns the possible errors

