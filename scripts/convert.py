"""
Convert different formats.

Take Gmail messages and convert them to something nicer, like MIME or HTML.
Or take something nicer like MIME or HTML and make it more readable.
"""
import base64
import email


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


def build_mime(content, email_address, filename):
    """
    For building a mime message to send.
    content: content of the email
    returns a mime document
    """
    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = email_address
    message['From'] = email_address
    message['Subject'] = filename
    message['Date'] = email.utils.formatdate(localtime=True)
    message['Message-ID'] = email.utils.make_msgid()
    message.set_content(content, subtype='html')
    return message


def html_to_mime(filename, email_address):
    """Read in HTML, return MIME ready to send."""
    f = open(filename, 'r', encoding="utf-8")
    mimedocument = build_mime(f.read(), email_address, filename)
    # data = f.read()
    # mimedocument.add_attachment(data)
    return mimedocument
