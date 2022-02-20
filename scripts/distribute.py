import glob
import json
import logging
import datetime
import os
import argparse
from jinja2 import Template

logging.basicConfig(level=logging.DEBUG)


def gather_from_files(pathname="experiments/*.json"):
    filenames = glob.glob(pathname)
    logging.debug(filenames)
    sheets = []
    for filename in filenames:
        sheet = read_json(filename)
        mandatory_keys = ["gmail_id", "body_html"]

        try:
            if all(key in sheet for key in mandatory_keys):
                sheets.append(sheet)
                logging.info("READ " + sheet["gmail_id"])
            else:
                logging.warning("COULD NOT PARSE: ", filename)
        except TypeError as e:
            logging.warning(filename + str(e))
    return sheets


def read_json(path):
    with open(path, "r") as infile:
        return json.load(infile)


def build_front_page(sheets, template):
    # Get a template file
    # Populate it with Jinja2
    pass


def generate_directory():
    rollname = datetime.date.today().isoformat()
    directory = "experiments/" + rollname + "/"
    if not os.path.isdir(directory):
        os.mkdir(directory)
    return directory


def write_pages(sheets, directory):
    """
    Writes HTML files to a directory, taking JSON sheets as input.

    :param sheets iterable: contains the keys 'body_html' and 'gmail_id'
    """
    for sheet in sheets:
        if type(sheet) == dict:
            path = generate_path(sheet, directory)
            if os.path.exists(path):
                logging.info(path + " already exists. Writing anyway.")
            with open(path, "w") as outfile:
                outfile.write(sheet["body_html"])
                logging.info("Writing " + path)
    return directory


def generate_path(sheet, directory):
    path = directory + sheet["gmail_id"] + ".html"
    return path


def files_to_pages():
    sheets = gather_from_files()
    directory = generate_directory()
    write_pages(sheets, directory)
    rendered = render_index(sheets, directory)
    write_index(rendered, directory)


def render_index(sheets, directory):
    pathnames = [sheet["gmail_id"] + ".html" for sheet in sheets]
    template_path = "./scripts/index.html.jinja"
    with open(template_path, "r") as infile:
        raw_template = infile.read()
    template = Template(raw_template)
    rendered = template.render(pathnames=pathnames)
    logging.info("Rendered template")
    return rendered


def write_index(templated, directory):
    path = directory + "/index.html"
    with open(path, "w") as outfile:
        outfile.write(templated)
        logging.info("Written to: " + path)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("function", help="function to run")
    parser.add_argument("--input", help="input for a function")
    args = parser.parse_args()
    if args.input:
        print(globals()[args.function](args.input))
    else:
        print(globals()[args.function]())
