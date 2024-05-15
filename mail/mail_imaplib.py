import imaplib
import email
import webbrowser
import os

#credentials
MAIL = "swallowspottesting@gmail.com"
__PASSWORD = "sgef pxbq ivqo dqpb"
IMAP_SERVER = "imap.gmail.com"

mail = imaplib.IMAP4_SSL(IMAP_SERVER)

def emials_fetch():
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
     
    #conversion form byte inconsistent data to email obj
    msg = email.message_from_bytes(raw_email)
     
    #extraction of trasmittion informations form obj (msg)
    sender = msg['From']
    subject = msg['Subject']
    body = None
    pdf = None
     
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if(content_type = "application/pdf" )
                pdf = part. 
                print("content type: ",content_type)
                content_disposition = str(part.get("Content-Disposition"))
                print("content disp: ",content_disposition)
                try:
                    body = part.get_payload(decode=True).decode()
                    print("body: ",body, "\n -------------------------")
                except:
                    print("non ho analizzato il part (body)")
                    pass
    else:
        body = msg.get_payload(decode=True).decode()
     
     print('From:', sender)
     print('Subject:', subject)
     print('Body:', body)
    
def main():
     #connection to imap server
     print("pronto per connetterti")
     mail.login(MAIL, __PASSWORD)
     print("ok connesso")
     emials_fetch()


if __name__ == '__main__':
    main()
else:    # close connection
    mail.close()
