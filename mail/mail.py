import imaplib
import email
from utils.bulletins_utils import save_bulletin
from time import sleep
import os

#JSON list allowed sender
allowed_senders = {
    "allowed_senders": [
        #"cmt.meteoveneto@arpa.veneto.it",
        #"info@aribassano.it",
        "centro.funzionale.server@regione.veneto.it",
        '"A.R.I. Bassano del Grappa" <info@aribassano.it>',
        '"centro.funzionale.server" <centro.funzionale.server@regione.veneto.it>',
    ]
}

# check sender function
def check_sender(msg):
    sender = msg.get('From', '')
    # print(sender)

    return sender in allowed_senders['allowed_senders']

def emails_fetch(mail):
    # select the mail's field where mails arrives
    mail.select("inbox")
    print("connected")
    # indexes all the msgs in the inbox
    status, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    # list the msgs indexed
    id_list= mail_ids.split()

    # for every id in mailbox fetch the relative data
    for num in id_list:
        status, data = mail.fetch(num, '(RFC822)')#std who define the format of mails for fetching to IMAP server
        raw_email = data[0][1]

        # conversion form byte inconsistent data to email obj
        msg = email.message_from_bytes(raw_email)
        # check if sender is permissed to being fetched
        if(check_sender(msg)):
            #print("it is")
            # extraction of trasmittion informations form obj (msg)
            sender = msg['From']
            subject = msg['Subject']
            body = None
            pdf = None
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if (content_type == "application/pdf"): # when occures attached as pdf then
                        #print ("found pdf")
                        pdf = part.get_payload(decode=True)
                        content_disposition = str(part.get("Content-Disposition"))
                        if "filename" in content_disposition:
                            filename = content_disposition.split("filename=")[1].strip().strip('"')
                        else:
                            filename = "attachment.pdf"  # Default filename if not specified
                        # print (filename)
                        result = save_bulletin(pdf, filename=filename)
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
            else:
                body = msg.get_payload(decode=True).decode()
            # sign the current mail as deletable
            # mail.store(num, '+FLAGS', '\Deleted')


        # deletes mails from not truster users (comment those lines to keep the mails of not trusted users)
        #else:
            #mail.store(num, '+FLAGS', '\Deleted')

        # delete the mails that has been signed
        #mail.expunge()

def get_emails():
    MAIL = os.getenv("MAIL")
    __PASSWORD = os.getenv("MAILPASSWORD")
    IMAP_SERVER = os.getenv("IMAPSERVER")
    #print("imap server", IMAP_SERVER)


    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    # connection to imap server
    mail.login(MAIL, __PASSWORD)
    emails_fetch(mail)
    mail.logout()


def start_cycle():
    while True:
        get_emails()
        sleep(60 * 30)

