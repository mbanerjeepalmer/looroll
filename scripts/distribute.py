import glob
import json
import logging
import datetime
import pdb
import os

logging.basicConfig(level=logging.DEBUG)


def gather_from_files(pathname="experiments/*.json"):
    filenames = glob.glob(pathname)
    sheets = [read_json(filename) for filename in filenames]
    return sheets


def read_json(path):
    with open(path, "r") as infile:
        return json.load(infile)


def build_front_page(sheets, template):
    # Get a template file
    # Populate it with Jinja2
    pass


def write_sheet_pages(sheets):
    rollname = datetime.date.today().isoformat()
    directory = "experiments/" + rollname + "/"
    if not os.path.isdir(directory):
        os.mkdir(directory)

    for sheet in sheets:
        if type(sheet) == dict:
            if all(key in sheet for key in ["gmail_id", "body_html"]):
                path = directory + sheet["gmail_id"] + ".html"

                if os.path.exists(path):
                    logging.info(path + " already exists. Writing anyway.")
                with open(path, "w") as outfile:
                    outfile.write(sheet["body_html"])
                    logging.info("Writing" + path)


def files_to_pages():
    sheets = gather_from_files()
    write_sheet_pages(sheets)


if __name__ == "__main__":
    files_to_pages()
