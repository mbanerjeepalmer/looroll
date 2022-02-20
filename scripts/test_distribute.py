import distribute
import json
import argparse
import pprint
import logging

pp = pprint.PrettyPrinter(indent=4)
logging.basicConfig(level=logging.DEBUG)


def test_gather_from_files():
    """Given a directory of JSON files it should be able to identify them
    based on a pattern and convert them into dictionaries."""
    # TODO get path from file https://stackoverflow.com/questions/50329629/how-to-access-a-json-filetest-data-like-config-json-in-conftest-py
    pieces = distribute.gather_from_files()
    assert len(pieces) > 0
    assert type(pieces[0]) == dict


def test_write_sheet_pages():
    pass


def test_render_template(tmpdir):
    sheets = [
        {"gmail_id": "1234abcd", "body_html": "<html><p>blah</p></html>"},
        {"gmail_id": "4321dcba", "body_html": "<html><p>bleh</p></html>"},
    ]
    templated = distribute.render_index(sheets, tmpdir.strpath)
    logging.debug(templated)
    assert len(templated) > 0


def test_build_front_page():
    """Given one or more dictionaries with some kind of heading,
    a name and body, build a page which displays the headings
    and links to the body."""
    pass


def test_build_piece_page():
    """Given a dictionary with a name and a body, write an HTML file with the
    body as the body and the name as the filename"""
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("function", help="function to run")
    parser.add_argument("--input", help="input for a function")
    args = parser.parse_args()
    if args.input:
        print(globals()[args.function](args.input))
    else:
        print(globals()[args.function]())
