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

# TODO Put this somewhere sensible
gmail_instance = gmail_access.gmail_setup()
filename = 'joinedemails/{0}-{1}-{2}-{3}.html'.format(*datetime.date.today().timetuple())
email_address = 'mbanerjeepalmer@gmail.com'
open(filename, 'w')  # TODO This is bad


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


def main(gmail_instance, filename, email_address,query='from:newsletter@crunchbase.com newer_than:30d'):
    """Get messages, store them and send them."""
    # TODO Loads of duplication in here.
    # Instead should be more functions inside functions?
    msg_ids = gmail_access.query_ids(gmail_instance, email_address, query)
    print(len(msg_ids))
    for msg_id in msg_ids:
        mimedocument = convert.new_better_mime_doc(gmail_instance, email_address, msg_id)
        write.append_html(mimedocument, filename)
        print(msg_id)
    sendable_mime = convert.html_to_mime(filename, email_address)
    gmail_access.hit_send(gmail_instance, sendable_mime)
    write.html_to_db(filename)

if __name__ == "__main__":
    main(gmail_instance, filename, email_address)
