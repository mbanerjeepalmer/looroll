"""Take stuff and read or write it to or from the database."""
import django
from loorollv2app.models import Roll


def append_html(mimedocument, filename):
    """Convert an email to HTML and write that locally."""
    try:
        html = mimedocument.get_body().get_content()
        # TODO Write to DB
        with open(filename, 'a', encoding="utf-8") as f:
            #TODO Tidy.
            f.write('\n')
            f.write(html)
            f.write('\n')
    except Exception as exception:
        # logging etc. needs fixing.
        # In past versions it used the apiclient errors
        print('Fuck. ' + str(exception))


def html_to_db(filename):
    django.setup()
    html = open(filename, 'r', encoding="utf-8").read()
    r = Roll(html_string=html)
    r.save()
