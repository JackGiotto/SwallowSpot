import imaplib
import email
import webbrowser
import os

#credentials
MAIL = "swallowspot@yahoo.com"
__PASSWORD = "RondineSpottatrice" #private variable
IMAP_SERVER = "imap.mail.yahoo.com"



def emials_fetch():
     mail = imaplib.IMAP4_SSL(IMAP_SERVER)

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
     
     if msg.is_multipart():
          for part in msg.walk():
               content_type = part.get_content_type()
               content_disposition = str(part.get("Content-Disposition"))
               try:
                    body = part.get_payload(decode=True).decode()
               except:
                    pass
     else:
          body = msg.get_payload(decode=True).decode()
     
     print('From:', sender)
     print('Subject:', subject)
     print('Body:', body)
     print('-' * 50)
    
def main():
     mail = imaplib.IMAP4_SSL(IMAP_SERVER)

     #connection to imap server
     print("pronto per connetterti")
     mail.login(MAIL, __PASSWORD)
     print("ok connesso")
     emials_fetch()


if __name__ == '__main__':
    main()
else:    # close connection
     mail.logout()

