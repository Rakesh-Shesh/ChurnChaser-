import smtplib
import imaplib
import email
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import decode_header
import os
import time
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Enable logging
logging.basicConfig(filename='automated_email_assistant.log', level=logging.DEBUG)

class AutomatedEmailAssistant:
    def __init__(self, email, password, use_oauth=False):
        self.email = email
        self.password = password
        self.use_oauth = use_oauth

        if self.use_oauth:
            self.service = self.authenticate_with_oauth()

        else:
            self.smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            self.smtp_server.starttls()
            self.smtp_server.login(email, password)
            self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com")

        logging.info(f"Assistant initialized for {self.email}")

    def authenticate_with_oauth(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('gmail', 'v1', credentials=creds)
        return service

    def send_email(self, receiver_email, subject, body, attachments=None):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as f:
                    attach_part = MIMEText(f.read(), 'base64', 'utf-8')
                    attach_part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
                    msg.attach(attach_part)

        try:
            if self.use_oauth:
                message = {'raw': msg.as_string()}
                self.service.users().messages().send(userId="me", body=message).execute()
            else:
                self.smtp_server.sendmail(self.email, receiver_email, msg.as_string())
            logging.info(f"Email sent to {receiver_email} with subject {subject}")

        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")

    def read_email(self, filter_by=None, mark_as_read=False):
        try:
            if self.use_oauth:
                results = self.service.users().messages().list(userId="me", q=filter_by).execute()
                messages = results.get('messages', [])
                if not messages:
                    logging.info("No new emails.")
                    return []
                message = self.service.users().messages().get(userId="me", id=messages[0]['id']).execute()
                payload = message['payload']
                headers = payload['headers']
                subject = next((item['value'] for item in headers if item['name'] == 'Subject'), 'No Subject')
                body = payload['body']['data']
                email_message = decode_header(subject)[0][0].decode('utf-8')
                return email_message
            else:
                self.imap_server.login(self.email, self.password)
                self.imap_server.select('inbox')

                result, data = self.imap_server.uid('search', None, "ALL")
                inbox_item_list = data[0].split()

                most_recent = inbox_item_list[-1]
                result2, email_data = self.imap_server.uid('fetch', most_recent, '(BODY.PEEK[])')

                raw_email = email_data[0][1].decode("utf-8")
                email_message = email.message_from_string(raw_email)
                if mark_as_read:
                    self.imap_server.uid('store', most_recent, '+FLAGS', '(\Seen)')
                return email_message

        except Exception as e:
            logging.error(f"Failed to read email: {str(e)}")
            return None

    def auto_reply(self, sender, subject, body):
        auto_reply = f"Thank you for your email. I am currently unavailable, but I will get back to you as soon as possible."
        self.send_email(sender, "Auto Response: " + subject, auto_reply)

    def schedule_email(self, receiver_email, subject, body, send_at_time):
        delay = send_at_time - datetime.now()
        if delay.total_seconds() > 0:
            logging.info(f"Email scheduled to send at {send_at_time}")
            time.sleep(delay.total_seconds())
            self.send_email(receiver_email, subject, body)
        else:
            logging.error("Scheduled time must be in the future!")

    def read_unread_emails(self):
        return self.read_email("is:unread")

# Example Usage
assistant = AutomatedEmailAssistant('youremail@gmail.com', 'yourpassword', use_oauth=True)

# Read recent email
print(assistant.read_email())

# Send an email with attachment
assistant.send_email('receiver@gmail.com', 'Subject Test', 'Body of the email', ['file1.pdf', 'file2.jpg'])

# Auto-reply
assistant.auto_reply('sender@example.com', 'Subject of incoming email', 'Body of incoming email')

# Schedule email
assistant.schedule_email('receiver@gmail.com', 'Scheduled Email', 'This is a scheduled email.', datetime(2024, 12, 25, 15, 0))

