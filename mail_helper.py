import imaplib
import imaplib
import re
from email import message_from_bytes, utils
from email.header import decode_header
import email
from email import utils

def decode_subject(encoded_subject):
    decoded_words = decode_header(encoded_subject)
    subject = ''.join([word.decode(encoding or 'utf-8') if isinstance(word, bytes) else word for word, encoding in decoded_words])
    return subject

def extract_email(string):
    # Regular expression to match an email
    email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    match = re.search(email_regex, string)
    if match:
        return match.group()
    return None

def fetch_emails(server, username, password, limit=50):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    mail.select('INBOX')

    # Fetch all emails and limit to the first 50 emails
    status, email_ids = mail.search(None, 'ALL')
    email_ids_list = email_ids[0].split()[:limit]

    emails = {}

    for email_id in email_ids_list:
        # Decode email_id if it's in bytes
        decoded_email_id = email_id.decode('utf-8') if isinstance(email_id, bytes) else str(email_id)
        status, email_data = mail.fetch(email_id, '(RFC822)')
        for response_part in email_data:
            if isinstance(response_part, tuple):
                email_message = email.message_from_bytes(response_part[1])

                email_details = {
                    'ID': decoded_email_id,
                    'From': extract_email(email_message['From']),
                    'Subject' : decode_subject(email_message['Subject']),
                    'Date': utils.parsedate_to_datetime(email_message['Date']).isoformat() if email_message['Date'] else None
                }
                emails[decoded_email_id] = email_details

    mail.logout()
    return emails


def delete_specific_email(server, username, password, email_id, permanent_remove = False):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    # Select the mailbox you want to access, typically INBOX
    mail.select('INBOX')
    # Iterate over each email ID from the list and mark them for deletion
    mail.store(email_id, '+FLAGS', '\\Deleted')  # Marks the email as deleted

    if permanent_remove:
        mail.expunge()
    # Logout and close connection
    mail.logout()
    return f"Email with ID {email_id} deleted"

def move_to_trash(server, username, password, email_id):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    mail.select('INBOX')
    # Copy to "Deleted Items" folder
    result = mail.copy(email_id, 'Deleted Items')
    # Check if the copy operation was successful
    if result[0] == 'OK':
        # Mark the email as deleted in the INBOX to simulate a "move" action
        mail.store(email_id, '+FLAGS', '\\Deleted')
        mail.expunge()
    
    # Close and logout from the server
    mail.close()
    mail.logout()
    return f"Email with ID {email_id} deleted"
