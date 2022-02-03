import glob
import json
import logging

logging.basicConfig(level=logging.DEBUG)


def gather_from_files(pathname="experiments/*.json"):
    filenames = glob.glob(pathname)
    pieces = [read_json(filename) for filename in filenames]
    logging.debug(pieces)
    return pieces


def read_json(path):
    with open(path, "r") as infile:
        return json.load(infile)


def build_front_page(pieces, template):
    # Get a template file
    # Populate it with Jinja2
    pass
