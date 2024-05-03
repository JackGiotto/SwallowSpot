
# process running in the server for Swallow Spot DB
""" 
import paramiko

# Informazioni di connessione al server MySQL remoto
remote_host = 'http://185.231.193.40:5006/'
remote_user = 'martini'
remote_password = 'martinid78'
remote_database = 'Swallow Spot'

# Impostazioni per la connessione SSH
ssh_host = '185.231.193.40'
ssh_user = 'martinidatabase'
ssh_password = 'martinid78'
ssh_port = 2234  # Porta SSH personalizzata

# Nome del file di dump
dump_file = 'backup.sql'

# Comando mysqldump da eseguire sul server remoto
mysqldump_cmd = f'mysqldump -u {remote_user} -p{remote_password} {remote_database} > {dump_file}'

# Connessione SSH al server
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

# Esegui il comando mysqldump sul server remoto
stdin, stdout, stderr = ssh_client.exec_command(mysqldump_cmd)

# Attendere il completamento del comando
stdout.channel.recv_exit_status()

# Chiudi la connessione SSH
ssh_client.close()

# Scarica il file di dump sul tuo computer locale
with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, username=ssh_user, password=ssh_password)
    sftp = ssh.open_sftp()
    sftp.get(dump_file, dump_file)

print("Backup completato!")
"""

"""     per connessione SSH ad un server
import paramiko

# Impostazioni per la connessione SSH
ssh_host = '185.231.193.40'
ssh_user = 'martinidatabase'
ssh_password = 'martinid78'
ssh_port = 2234  # Porta SSH personalizzata

# Crea un oggetto SSHClient
ssh_client = paramiko.SSHClient()

# Imposta la politica per gestire automaticamente le chiavi degli host mancanti
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connettiti al server SSH specificando la porta personalizzata
ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, password=ssh_password)

# Ora puoi eseguire comandi SSH o altre operazioni utilizzando ssh_client
#

# Quando hai finito, ricorda di chiudere la connessione
ssh_client.close() 
"""

""" import paramiko
import mysql.connector
import os

# Parametri di connessione al server SSH
ssh_host = 'hostname_or_ip_address'
ssh_port = 22
ssh_username = 'your_ssh_username'
ssh_password = 'your_ssh_password'

# Parametri di connessione al database MySQL
db_host = 'database_hostname_or_ip_address'
db_user = 'your_database_username'
db_password = 'your_database_password'
db_name = 'your_database_name'

# Nome del file SQL da inviare al server SSH
sql_file = 'backup.sql'

# Connessione al database MySQL e creazione del file SQL
try:
    # Connessione al database
    conn = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = conn.cursor()

    # Esempio di query per ottenere il dump del database in un file SQL
    dump_command = f"mysqldump -u {db_user} -p{db_password} {db_name} > {sql_file}"
    os.system(dump_command)

    # Chiudi la connessione al database
    cursor.close()
    conn.close()

    print(f'Backup del database {db_name} completato con successo')

    # Connessione al server SSH
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

    # Trasferimento del file SQL al server SSH
    with open(sql_file, 'rb') as f:
        ssh_client.exec_command(f'mkdir -p /path/to/save/backups')
        ssh_client.exec_command(f'cd /path/to/save/backups && touch {sql_file}')
        sftp_client = ssh_client.open_sftp()
        sftp_client.putfo(f, f'/path/to/save/backups/{sql_file}')

    print(f'File {sql_file} inviato con successo al server SSH')

    # Chiudi la connessione SSH
    ssh_client.close()

except mysql.connector.Error as e:
    print(f'Errore durante il backup del database: {e}')

except paramiko.SSHException as e:
    print(f'Errore durante la connessione SSH: {e}')

except Exception as e:
    print(f'Errore generico: {e}') """


# mysqldump -u martini -p "Swallow Spot" > backup.sql


import socket
import ssl

ip_addr = '192.168.0.100'

# Create an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

context.load_verify_locations("certificate/server.crt")

# Connect to the server
ssl_client_socket = context.wrap_socket(client_socket, server_hostname="localhost")
ssl_client_socket.connect((ip_addr, 8080))

# Send data
ssl_client_socket.send("Hello from client!".encode())

# Receive response
response = ssl_client_socket.recv(1024)
print("Response from server:", response.decode())

# Close the connection
ssl_client_socket.close()



"""
import ssl
import socket

if __name__ == "__main__":
    # Create a context, just like as for the server
    context = ssl.create_default_context()
    # Load the server's CA
    context.load_verify_locations("certificate/server.crt")
    
    # Wrap the socket, just as like in the server.
    conn = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname="localhost")
    
    # Connect and send data! Standard python socket stuff can go here.
    conn.connect(("localhost", 8080))
    conn.sendall(b"Hello, server! This was encrypted.")
"""
