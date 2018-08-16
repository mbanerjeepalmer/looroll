"""Accesses Gmail and finds or sends emails."""
import base64
import os
from requests_oauthlib import OAuth2Session
# TODO from oauthlib.oauth2 import TokenExpiredError
import requests
import email


client_secret = os.environ['GOOGLE_CLIENT_SECRET']
client_id = os.environ['GOOGLE_CLIENT_ID']

scope = 'https://www.googleapis.com/auth/gmail.modify'
redirect_uri = 'https://127.0.0.1:8000/auth/complete/google-oauth2/'
authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
access_type = 'offline'
prompt = 'select_account'
token_url = 'https://www.googleapis.com/oauth2/v4/token'

# TODO Restructure all this so that it's not duplicating effort each time etc.


def user_oauth():
    client = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = client.authorization_url(authorization_base_url,
        access_type='offline', prompt='select_account')
    return authorization_url, state


def server_oauth(authorization_response):
    client = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    token = client.fetch_token('https://accounts.google.com/o/oauth2/token',
        authorization_response=authorization_response,
        client_secret=client_secret)
    return token    # Check refresh token, change prompt to 'consent' if not

def refresh_access_token(token):
    #TODO change to https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#third-recommended-define-automatic-token-refresh-and-update
    extra = {'client_id': client_id, 'client_secret': client_secret}
    client = OAuth2Session(client_id,scope=scope,redirect_uri=redirect_uri, token=token) # TODO Work out what to do about long lines...
    token = client.refresh_token(token_url, **extra)
    return token, client

def test_request(client):
    protected_url = 'https://www.googleapis.com/gmail/v1/users/mbanerjeepalmer@gmail.com/messages'
    r = client.get(protected_url)
    return r.status_code

def gmail_query(client, user_id, query):
    #TODO use label parameter rather than pack it into the query, maybe
    params = {'q': query}
    r = client.get('https://www.googleapis.com/gmail/v1/users/{}/messages'.format(user_id), params=params)
    #TODO Handle multiple pages
    r.raise_for_status()
    results = r.json()
    if results['resultSizeEstimate'] > 0:
        msg_ids = [i['id'] for i in results['messages']]
        return msg_ids
    else:
        print('Nothing here')


def get_email_body(client, user, msg_id):
    # TODO inevitably most of this is going to be unnecessary
    # It will simply turn out that I can get HTML straight away...
    body = client.get('https://www.googleapis.com/gmail/v1/users/{}/messages/{}'.format(user, msg_id), params={'format':'raw'}).json()
    raw_body = body['raw']
    msg_str = base64.urlsafe_b64decode(raw_body.encode('ASCII'))
    msg_parser = email.parser.BytesFeedParser(policy=email.policy.default)
    msg_parser.feed(msg_str)
    mimedocument = msg_parser.close()
    return mimedocument

def write_local_html(mimedocument, filename):
    # TODO either put everything in the same module, or bin this once the write module is working again
    """Convert an email to HTML and write that locally."""
    try:
        html = mimedocument.get_body().get_content()
        with open(filename, 'a', encoding="utf-8") as f:
            #TODO Tidy.
            f.write('\n')
            f.write(html)
            f.write('\n')
    except Exception as exception:
        # TODO logging etc. needs fixing.
        # In past versions it used the apiclient errors
        print('Fuck. ' + str(exception))


def new_better_mime_doc(service, user_id, msg_id):
    """Take a gmail message id and returns the MIME document."""
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()  # TODO split the line
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        msg_parser = email.parser.BytesFeedParser(policy=email.policy.default)
        msg_parser.feed(msg_str)
        mimedocument = msg_parser.close()
        return mimedocument
    except:
        # TODO Fix error handling. How come it worked before?
        print('An error occurred.')


def send_email(access_token, mime_doc):
    pass



# SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
# redirect_uri = 'http://127.0.0.1:8000/rolls/'
# # TODO Enable offline access
#
# # flow = OAuth2WebServerFlow(client_id=client_id,
#                            client_secret=client_secret,
#                            scope=SCOPES,
#                            redirect_uri=redirect_uri)
#
# auth_uri = flow.step1_get_authorize_url()
#
# # TODO receive authorization code. Would that just be a post request?
#
# def gmail_setup():
#     """Return a Gmail instance."""
#     SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
#     store = file.Storage(os.path.abspath('.\\secrets\\storage.json'))
#     creds = store.get()
#     if not creds or creds.invalid:
#         # TODO I don't believe this fully works.
#         # At the moment I need to delete 'storage.json' to trigger this flow.
#         flow = client.flow_from_clientsecrets(os.path.abspath('.\\secrets\\client_secret.json'), SCOPES)
#         creds = tools.run_flow(flow, store)
#     return discovery.build('gmail', 'v1', http=creds.authorize(Http()))


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
