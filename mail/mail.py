import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
def authenticate():
    scope=['https://www.googleapis.com/auth/gmail.readonly']

    # Load credentials from file
    credentials = None
    if os.path.exists('credentials.json'):
        credentials = Credentials.from_authorized_user_file('credentials.json')

    # If credentials are expired or missing, refresh or request new ones
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            InstalledAppFlow.from_client_secrets_file("./secret.json", scopes=scope)
            credentials = flow.run_local_server(port=0)

        # Save credentials to file
        with open('credentials.json', 'w') as credentials_file:
            credentials_file.write(credentials.to_json())

    return credentials
"""
def list_messages(service, user_id='me'):
    try:
        # List messages from inbox
        response = service.users().messages().list(userId=user_id, labelIds=['INBOX']).execute()
        messages = response.get('messages', [])

        if messages:
            for message in messages:
                msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
                print('Message snippet: {}'.format(msg['snippet']))

    except HttpError as error:
        print('An error occurred: {}'.format(error))"""

def get_emails(credentials, service):
    # Chiamata all'API di Gmail per ottenere le email
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        print("Nessuna email trovata.")
    else:
        print("Elenco delle email:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            # Decodifica il corpo del messaggio
            raw_data = msg['payload']['parts'][0]['body']['data']
            message_body = base64.urlsafe_b64decode(raw_data).decode('utf-8')
            print("From:", msg['payload']['headers'][17]['value'])
            print("Subject:", msg['payload']['headers'][19]['value'])
            print("Body:", message_body)
            print("---------------------------------------")

def main():
    # Authenticate with Gmail API
    credentials = authenticate()
    service = build('gmail', 'v1', credentials=credentials)

    # Continuously read emails
    while True:
        get_emails(credentials, service)
        time.sleep(60)  # Check for new emails every minute
    service.close()

if __name__ == '__main__':
    main()
