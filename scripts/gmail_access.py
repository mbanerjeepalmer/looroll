"""Accesses Gmail and finds or sends emails."""
from apiclient import discovery
from oauth2client import file, client, tools
from httplib2 import Http
import base64


def gmail_setup():
    """Return a Gmail instance."""
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
    store = file.Storage('.\\secrets\\storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        # TODO I don't believe this fully works.
        # At the moment I need to delete 'storage.json' to trigger this flow.
        flow = client.flow_from_clientsecrets('.\\secrets\\client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return discovery.build('gmail', 'v1', http=creds.authorize(Http()))


def query_ids(service, user_id, query):
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
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        ids = []
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])
        for message in messages:
            ids.append(message['id'])
        return ids
    except:
        #TODO Handle errors
        print('An error occurred.')


def hit_send(service, mimedocument):
    """
    Send an email.

    Service: Authorized Gmail API service instance.
    Mimedocument: the file created in buildmime.
    """
    body = {'raw': base64.urlsafe_b64encode(mimedocument.as_bytes()).decode()}
    messages = service.users().messages()
    messages.send(userId='me', body=body).execute()
    print('Email sent')
