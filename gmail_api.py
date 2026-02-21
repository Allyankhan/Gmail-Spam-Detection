import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Shows basic usage of the Gmail API. Lists the user's Gmail labels."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def get_recent_emails(service, max_results=10):
    """Fetches a list of recent emails."""
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    
    email_list = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = msg_data['payload']['headers']
        
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), "Unknown Sender")
        date = next((h['value'] for h in headers if h['name'].lower() == 'date'), "Unknown Date")
        
        email_list.append({
            'id': msg['id'],
            'subject': subject,
            'sender': sender,
            'date': date,
            'payload': msg_data['payload']
        })
    return email_list

def extract_email_data(service, payload, message_id):
    """Recursively extracts body text and attachment details from an email payload."""
    body_text = ""
    attachments = []

    def parse_parts(parts):
        nonlocal body_text, attachments
        for part in parts:
            mime_type = part.get('mimeType')
            body = part.get('body')
            data = body.get('data')
            attachment_id = body.get('attachmentId')

            # Extract Text
            if mime_type == 'text/plain' and data:
                body_text += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore') + "\n"
            elif mime_type == 'text/html' and data:
                html_data = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html_data, 'html.parser')
                body_text += soup.get_text() + "\n"

            # Extract Attachments
            if attachment_id:
                attachments.append({
                    'filename': part.get('filename'),
                    'attachmentId': attachment_id,
                    'messageId': message_id
                })
            
            # Recursive call for nested parts (like multipart/alternative)
            if 'parts' in part:
                parse_parts(part['parts'])

    if 'parts' in payload:
        parse_parts(payload['parts'])
    else:
        # Sometimes payload has no parts, just the body
        parse_parts([payload])

    return body_text.strip(), attachments

def download_attachment(service, message_id, attachment_id):
    """Downloads attachment bytes securely."""
    attachment = service.users().messages().attachments().get(
        userId='me', messageId=message_id, id=attachment_id
    ).execute()
    file_data = base64.urlsafe_b64decode(attachment['data'])
    return file_data