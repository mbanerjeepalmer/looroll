import datetime
import json
import email
import logging
import base64
from email.policy import default

logging.basicConfig(level=logging.DEBUG)


def orchestrate_ingestion(client):
    message_result = pull_from_gmail(client)
    logging.info("Pulled from Gmail")
    logging.debug(message_result)
    parsed_emails = get_all_emails(client, message_result)
    logging.info("Writing emails locally")
    for parsed_email in parsed_emails:
        path = write_complete_email_locally(parsed_email)
        logging.info("Wrote " + path)


def pull_from_gmail(client, query_string="newer_than:7d"):
    """
    Returns the result of `query_gmail` using `query_string`,
    which is a  list of IDs as strings.

    :param client OAuth2Session object: Authenticated session.
    :param query_string string: Gmail-compatible string.
    """
    try:
        params = {"q": query_string}
        return gmail_request(client, params=params)
    except Exception as e:
        print(e)


def query_gmail(client, query_string):
    """
    Returns a list of results by executing the `query_string`
    against messages on the Gmail API.

    :param client OAuth2Session object: Authenticated session.
    :param query_string string: Gmail-compatible string.
    """
    query_url = "https://www.googleapis.com/gmail/v1/users/me/messages"
    request = client.get(query_url, params={"q": query_string})
    request.raise_for_status()
    results = request.json()
    logging.debug(results)
    return results


def write_string_locally(string, name_prefix="", extension="", base_path=""):

    if name_prefix:
        name_prefix = name_prefix + "-"
    formatted_time = datetime.datetime.now().isoformat()
    filename = "{name_prefix}{formatted_time}.{extension}".format(
        name_prefix=name_prefix, formatted_time=formatted_time, extension=extension
    )
    if not base_path:
        base_path = "./experiments"
    path = base_path + "/" + filename

    with open(path, "w") as outfile:
        outfile.write(string)
    return path


def write_complete_email_locally(parsed_email, base_path=""):
    name_prefix = "complete-{}".format(parsed_email["gmail_id"])
    return write_string_locally(
        json.dumps(parsed_email),
        name_prefix=name_prefix,
        extension="json",
        base_path=base_path,
    )


def write_email_body_locally(parsed_email):
    name_prefix = "{}-{}".format(parsed_email["gmail_id"], parsed_email["Received"])
    return write_string_locally(
        parsed_email["body_html"], name_prefix=name_prefix, extension="html"
    )


def get_email(client, message_id, user="me"):
    message = gmail_request(client, message_id=message_id, params={"format": "raw"})
    raw_body = message["raw"]
    msg_str = base64.urlsafe_b64decode(raw_body.encode("ASCII"))
    msg_parser = email.parser.BytesFeedParser(policy=default)
    msg_parser.feed(msg_str)
    mimedocument = msg_parser.close()
    headers = dict(mimedocument)
    body_html = mimedocument.get_body().get_content()
    parsed_email = {"body_html": body_html, "gmail_id": message_id, **headers}
    return parsed_email


def get_all_emails(client, query_results):
    """
    Returns a list of dictionaries.

    :param client [TODO:type]: [TODO:description]
    :param query_results [TODO:type]: [TODO:description]
    """
    message_ids = [message["id"] for message in query_results["messages"]]
    parsed_emails = []
    for message_id in message_ids:
        try:
            parsed_email = get_email(client, message_id)
            parsed_emails.append(parsed_email)
        except KeyError as e:
            logging.error("Could not parse email", message_id, e)
    return parsed_emails


def gmail_request(client, user="me", params=None, message_id=None):
    endpoint = "https://www.googleapis.com/gmail/v1/users/{user}/messages{message_id}"
    if message_id:
        message_suffix = "/" + message_id
    else:
        message_suffix = ""
    url = endpoint.format(user=user, message_id=message_suffix)
    response = client.get(url, params=params)
    response.raise_for_status()
    return response.json()
