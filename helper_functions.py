import json
from bs4 import BeautifulSoup

def extract_text_from_emails(email_data):
    ''' gets the text from the emails and returns a list of dictionaries with the cleaned data '''
    cleaned_emails = []

    for email in email_data:
        # Initialize cleaned email data
        cleaned_email = {
            'From': email['From'],
            'Subject': email['Subject'],
            'Date': email['Date'],
            'Body': ''
        }

        # Check if the body is HTML or plain text and clean accordingly
        if '<html>' in email['Body'].lower() or '<body>' in email['Body'].lower():
            soup = BeautifulSoup(email['Body'], 'html.parser')
            cleaned_email['Body'] = soup.get_text()
        else:
            cleaned_email['Body'] = email['Body']

        cleaned_emails.append(cleaned_email)

    return cleaned_emails