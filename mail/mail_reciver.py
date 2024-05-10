from aspose.email import ImapClient

#credentials
MAIL = "swallowspot@yahoo.com"
__PASSWORD = "RondineSpottatrice" #private variable
IMAP_SERVER = "imap.mail.yahoo.com"
PORT = 993

# Make a connection with IMAP server
with ImapClient(IMAP_SERVER, PORT, MAIL, __PASSWORD) as conn:

    # Select folder
    conn.select_folder("Inbox")

    # List messages
    for msg in conn.list_messages():

        # Save message
        conn.save_message(msg.unique_id, msg.unique_id + "_out.eml")
        
print("ci siamo?")