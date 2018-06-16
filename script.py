#!/usr/bin/python3.6
import os
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import email.message, email.policy, email.utils, sys
import base64
import datetime
import requests
from bs4 import BeautifulSoup
import django

SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
store = file.Storage('secrets/storage.json')
creds = store.get()
if not creds or creds.invalid: # I don't believe this fully works. At the moment I need to delete 'storage.json' to trigger this flow.
    flow = client.flow_from_clientsecrets('secrets/client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)

GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
filename = 'joinedemails/{0}-{1}-{2}.html'.format(*datetime.date.today().timetuple())

def ListMessagesMatchingQuery(service, user_id, query='list@ben-evans.com'):
    """List all Messages of the user's mailbox matching the query.
    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.
    Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,pageToken=page_token).execute()
            messages.extend(response['messages'])
        return messages
    except errors.HttpError as error:
        print ('An error occurred: {}'.format(error))

def new_better_mime_message(service, user_id, msg_id):
    """
    Takes a message id and returns the MIME document
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,format='raw').execute()
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
    except errors.HttpError as error:
        print ('An error occurred:  {}'.format(error))
    msg_parser = email.parser.BytesFeedParser(policy=email.policy.default)
    msg_parser.feed(msg_str)
    mimedocument = msg_parser.close()
    return mimedocument

def write_html(mimedocument):
    try:
        html = mimedocument.get_body().get_content()
        with open (filename, 'a', encoding="utf-8") as f:
            f.write('\n')
            f.write(html)
            f.write('\n')
    except Exception as exception:
        print ('Fuck.' + str(exception))


def build_mime(content):
    """
    content: content of the email
    returns a mime document
    """
    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = 'mbanerjeepalmer@gmail.com'
    message['From'] = 'Test Sender <joebloggsspameggs@gmail.com>'
    message['Subject'] = filename
    message['Date'] = email.utils.formatdate(localtime=True)
    message['Message-ID'] = email.utils.make_msgid()
    message.set_content(content, subtype='html')
    return message

def hit_send(service, mimedocument):
    """
    service: Authorized Gmail API service instance.
    mimedocument: the file created in buildmime
    """
    body = {'raw': base64.urlsafe_b64encode(mimedocument.as_bytes()).decode()}
    messages = service.users().messages()
    send = messages.send(userId='me', body=body).execute()
    print ('Email sent')

def great_search():
    # this needs a query argument
    query = 'label:unroll.me newer_than:1d'
    messages = ListMessagesMatchingQuery(GMAIL, 'me', query)
    identities = []
    for message in messages:
        identities.append(message['id'])
    return identities

def getevents():
    r = requests.get('http://www.lse.ac.uk/Events/Search-Events')
    soup = BeautifulSoup(r.text, 'html.parser')
    event_results = soup.find(class_='largeList').get_text()
    with open(filename, 'w', encoding="utf-8") as outfile:
        outfile.write(event_results)
    print ('Events saved.')
    # events =
    # for e in events:
    # also put in the html2text

def plain_text_parser():
    pass
    #html2text goes here

def if_name_equals_main_should_probably_be_used_here():
    f = open(filename, 'w')
    # getevents()
    message_ids = great_search()
    print (len(message_ids))
    for message_id in message_ids:
        mimedocument = new_better_mime_message(GMAIL, 'me', message_id)
        write_html(mimedocument)
        print (message_id)
    f = open(filename, 'r', encoding="utf-8")
    mimedocument = build_mime(f.read())
    data = f.read()
    mimedocument.add_attachment(data)
    hit_send(GMAIL, mimedocument)

if_name_equals_main_should_probably_be_used_here()

# this should definitely be split out
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loorollv2.settings')
django.setup()
from loorollv2app.models import Roll

html = open(filename, 'r', encoding="utf-8")
r = Roll(html_string=html)
r.save()
