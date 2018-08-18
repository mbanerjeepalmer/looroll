"""Pull together the different functions etc and execute."""
# !/usr/bin/python3.6
# TODO decide whether shebang is necessary
import os
#TODO See if I can move this elsewhere.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loorollv2.settings")
import django
django.setup()
import datetime
from scripts import convert, gmail_access, write
import ast

user = os.environ['TEST_EMAIL_ADDRESS']
token = {
    'access_token': '',
    'token_type': 'Bearer',
    'expires_in': 3600,
    'refresh_token': os.environ['GOOGLE_REFRESH_TOKEN'],
    'scope': ['https://www.googleapis.com/auth/gmail.modify'],
    'expires_at': 1533628462.5902889
}

#
#
# # TODO Put this somewhere sensible
# gmail_instance = gmail_access.gmail_setup()
# filename = 'joinedemails/{0}-{1}-{2}-{3}.html'.format(*datetime.date.today().timetuple())
# open(filename, 'w')  # TODO This is bad
#

# The structure is:
# Define what I'm doing
#     - This means what's the scope (date, user)
#     - Where is it being stored
# Go and get the appropriate messages
#     - Get message IDs
#     - Convert message IDs to MIME
#     - Convert MIME to HTML
# Do something with those messages
#     - Store the roll of them in the database
#     - Email the roll

#
# def main(gmail_instance, filename, email_address,query='from:newsletter@crunchbase.com newer_than:30d'):
#     """Get messages, store them and send them."""
#     # TODO Loads of duplication in here.
#     # Instead should be more functions inside functions?
#     msg_ids = gmail_access.query_ids(gmail_instance, email_address, query)
#     print(len(msg_ids))
#     for msg_id in msg_ids:
#         mimedocument = convert.new_better_mime_doc(gmail_instance, email_address, msg_id)
#         write.append_html(mimedocument, filename)
#         print(msg_id)
#     sendable_mime = convert.html_to_mime(filename, email_address)
#     gmail_access.hit_send(gmail_instance, sendable_mime)
#     write.html_to_db(filename)
#
# if __name__ == "__main__":
#     main(gmail_instance, filename, email_address)
#
#
#
#
# BIN THIS. NEW, BETTER VERSION.

# The structure is:
# Define what I'm doing
#     - This means what's the scope (date, user)
#     - Where is it being stored
# Go and get the appropriate messages
#     - Get message IDs
#     - Convert message IDs to MIME
#     - Convert MIME to HTML
# Do something with those messages
#     - Store the roll of them in the database
#     - Email the roll


# Define what I'm doing
#     - This means what's the scope (date, user, emails)
#         - Date `newer than 1d`
#         - User - only one for the moment
#         - Emails sender in list or label
#             - Label approach
#             - Set label
#                 - Set manually at first
#                 - Set programmatically later
#             - Retrieve by label
#                 - Basic
#                     - Gmail 'label:looroll'
#                 - Clever way (too clever maybe)
#                     - Note that the steps are
#                         - Get list of all Gmail labels
#                         - Find the one which has the appropriate name
#                         - Get the immutable ID  for that label. Maybe. Otherwise I could just use Gmail query.
#                 - Can use previous approach for this
#
# - Where is it being stored


def main(token):
    token, client = gmail_access.refresh_access_token(token)
    msg_ids = gmail_access.gmail_query(client, user, 'newer_than:1d label:looroll')
    for msg_id in msg_ids:
        mimedocument = gmail_access.get_email_body(client, user, msg_id)
        write.html_to_db(mimedocument)
        print(msg_id)
    print ('Done')

if __name__ == "__main__":
    main(token)
