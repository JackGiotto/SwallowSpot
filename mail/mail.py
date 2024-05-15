import imaplib
import email
from utils.bulletins_utils import save_bulletin
from time import sleep
import os

#credentials


def emails_fetch(mail):
    #select the mail's field where mails arrives
    mail.select("inbox")

    #indexes all the msgs in the inbox
    status, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    #list the msgs indexed
    id_list= mail_ids.split()

    #for every id in mailbox fetch the relative data 
    for num in id_list:
        status, data = mail.fetch(num, '(RFC822)')#std who define the format of mails for fetching to IMAP server
        raw_email = data[0][1]
     
        # conversion form byte inconsistent data to email obj
        msg = email.message_from_bytes(raw_email)
        
        # extraction of trasmittion informations form obj (msg)
        sender = msg['From']
        subject = msg['Subject']
        body = None
        pdf = None
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if (content_type == "application/pdf"): # when occures attached as pdf then
                    pdf = part.get_payload(decode=True)
                    content_disposition = str(part.get("Content-Disposition"))
                    if "filename" in content_disposition:
                        filename = content_disposition.split("filename=")[1].strip().strip('"')
                    else:
                        filename = "attachment.pdf"  # Default filename if not specified
                    print("Content type:", content_type)
                    print("Type:", type(pdf))
                    result = save_bulletin(pdf, filename=filename)
                    print(result)
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
        else:
            body = msg.get_payload(decode=True).decode()
        
        mail.store(num, '+FLAGS', '\Deleted')
        print('From:', sender)
        print('Subject:', subject)
        print('Body:', body)

    mail.expunge()
    
def get_emails():
    MAIL = "swallowspottesting@gmail.com"
    __PASSWORD = "sgef pxbq ivqo dqpb"
    IMAP_SERVER = "imap.gmail.com"

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    #connection to imap server
    print("pronto per connetterti")
    mail.login(MAIL, __PASSWORD)
    print("ok connesso")
    emails_fetch(mail)


def start_cycle():
    while True:
        get_emails()
        sleep(60 * 30)

"""
if __name__ == '__main__':
    main()
else:    # close connection
    mail.close()
"""
