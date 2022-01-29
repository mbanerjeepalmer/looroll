"""Main file for  running the new aggregation process
"""

def main():
    source_content = pull_from_gmail()

def pull_from_gmail():
    authentication = authenticate_gmail()
    content = pull_gmail_content()
    normalise_gmail()

    return content

def selected_content():
    select kkk
