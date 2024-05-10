import imaplib
import email
from email.header import decode_header

# Funzione per decodificare l'intestazione dell'email
def decode_email_header(header):
    decoded_parts = decode_header(header)
    decoded_text = []
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_text.append(part.decode(encoding or 'utf-8'))
        elif isinstance(part, str):
            decoded_text.append(part)
    return ' '.join(decoded_text)

# Connessione al server IMAP di Yahoo
imap_server = 'imap.mail.yahoo.com'
port = 993
username = 'swallowspot@yahoo.com'
password = 'RondineSpottatrice'

mail = imaplib.IMAP4_SSL(imap_server, port)
mail.login(username, password)

# Selezione della casella di posta (IMAP usa 'INBOX' come cartella predefinita)
mail.select('INBOX')

# Ricerca delle email nella casella di posta
status, messages = mail.search(None, 'ALL')
if status == 'OK':
    # Elenco dei numeri delle email
    messages = messages[0].split()

    for msg_id in messages:
        # Recupero dell'email
        status, msg = mail.fetch(msg_id, '(RFC822)')
        if status == 'OK':
            email_data = msg[0][1]
            raw_email = email.message_from_bytes(email_data)

            # Recupero delle informazioni sull'email
            sender = decode_email_header(raw_email['From'])
            subject = decode_email_header(raw_email['Subject'])
            date = decode_email_header(raw_email['Date'])
            
            print('From:', sender)
            print('Subject:', subject)
            print('Date:', date)

            # Recupero del corpo del messaggio
            if raw_email.is_multipart():
                for part in raw_email.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                        print('Body:', body)
            else:
                body = raw_email.get_payload(decode=True).decode()
                print('Body:', body)

# Disconnessione dal server IMAP
mail.logout()
