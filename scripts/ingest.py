import datetime
import json


def pull_from_gmail(client):
    try:
        query_string = "newer_than:1d"
        return query_gmail(client, query_string)
    except Exception as e:
        print(e)


def query_gmail(client, query_string):
    query_url = "https://www.googleapis.com/gmail/v1/users/me/messages"
    params = {"q": query_string}
    request = client.get(query_url, params=params)
    request.raise_for_status()
    results = request.json()
    return results


def write_results_locally(result, path_template=None):
    if path_template is None:
        path_template = "gmail-results-{}.json"
    formatted_time = datetime.datetime.now().isoformat()
    path = path_template.format(formatted_time)
    with open(path, "w") as outfile:
        outfile.write(json.dumps(result))
