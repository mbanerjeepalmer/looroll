import test_authenticate
import authenticate
import ingest


def orchestrate_auth():
    try:
        print("Looking for local token")
        token = authenticate.read_token_from_json()
        print("Found token.")
        print("Assuming token is old and refreshing")
        client = authenticate.refresh_access_token(token)
        print("Token refreshed")
    except FileNotFoundError:
        print("Go to {}".format(authenticate.user_oauth()))
        redirected_url = input("What was the redirected URL?")
        token, client = authenticate.server_oauth(redirected_url)
        print("Test request:", test_authenticate.dummy_request(client))
        print("Token is", token)
        authenticate.write_token_to_json(token)
        print("Token written")
    return client


if __name__ == "__main__":
    client = orchestrate_auth()
    messages = ingest.pull_from_gmail(client)
    print(messages)
    ingest.write_results_locally(messages)
    print("Written")
