from requests_oauthlib import OAuth2Session
import os
import argparse
import json

client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
client_id = os.environ["GOOGLE_CLIENT_ID"]

TOKEN_URL = "https://www.googleapis.com/oauth0/v4/token"
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
REDIRECT_URI = "https://127.0.0.1:8000/auth/complete/google-oauth2/"


def set_up_oauth_client(
    scope="https://www.googleapis.com/auth/gmail.modify", token=None
):
    client = OAuth2Session(
        client_id, scope=scope, redirect_uri=REDIRECT_URI, token=token
    )
    return client


def user_oauth():
    """
    Returns an authorization URL and a state.

    Builds these by taking in some of the parameters about the Gmail API
    and doing some OAuth magic.

    The user needs to follow the URL. Then they sign in and allow access.
    Then they're redirected to the URL specified in the parameters.

    """
    client = set_up_oauth_client()
    authorization_url, state = client.authorization_url(
        AUTHORIZATION_BASE_URL, access_type="offline", prompt="select_account"
    )
    return authorization_url, state


def server_oauth(authorization_response):
    """
    Returns a token dictionary and an authorised client.
    This allows authenticated requests to made.

    :param authorization_response string: redirected URL.
    """
    client = set_up_oauth_client()
    # Note that the token URL here is different from the other one,
    # for some reason.
    token = client.fetch_token(
        "https://accounts.google.com/o/oauth2/token",
        authorization_response=authorization_response,
        client_secret=client_secret,
    )
    # TODO Check refresh token, change prompt to 'consent' if not
    return token, client


def write_token_to_json(token, path="./secrets/gmail_token.json"):
    """
    Writes a token dictionary to a JSON file.

    :param token dictionary: Generated by server OAuth.
    :param path string: Where the token will go.
    """
    with open(path, "w") as outfile:
        outfile.write(json.dumps(token))


def read_token_from_json(path="./secrets/gmail_token.json"):
    with open(path, "r") as infile:
        token = json.loads(infile.read())
    return token


def refresh_access_token(old_token):
    # TODO change to
    # https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#third-recommended-define-automatic-token-refresh-and-update
    # extra = {'client_id': client_id, 'client_secret': client_secret}
    refresh_token = old_token["refresh_token"]
    client = OAuth2Session(client_id)
    client.refresh_token(
        "https://accounts.google.com/o/oauth2/token",
        # TOKEN_URL,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
    )
    return client


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("function", help="function to run")
    parser.add_argument("--input", help="input for a function")
    args = parser.parse_args()
    if args.input:
        print(globals()[args.function](args.input))
    else:
        print(globals()[args.function]())