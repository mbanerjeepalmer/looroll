"""Take stuff and read or write it to or from the database."""
import django
from loorollv2app.models import Roll
import datetime


def append_html(mimedocument, filename):
    """Convert an email to HTML and write that locally."""
    try:
        html = mimedocument.get_body().get_content()
        with open(filename, 'a', encoding="utf-8") as f:
            # TODO Tidy.
            f.write('\n')
            f.write(html)
            f.write('\n')
    except Exception as exception:
        # TODO logging etc. needs fixing.
        # In past versions it used the apiclient errors
        print('Fuck. ' + str(exception))


def html_to_db(mimedocument):
    html = mimedocument.get_body().get_content()
    # TODO Better option should be the F thing and/or Concat:
    # https://docs.djangoproject.com/en/2.0/ref/models/database-functions/#django.db.models.functions.Concat
    # https://docs.djangoproject.com/en/2.0/ref/models/expressions/#django.db.models.F
    # https://docs.djangoproject.com/en/2.0/topics/db/queries/#topics-db-queries-update
    django.setup()
    today_roll = Roll.objects.latest(field_name='created_date')
    if today_roll.created_date.date() != datetime.date.today():
        Roll(html_string='')
    today_roll = Roll.objects.latest(field_name='created_date')
    today_html = today_roll.html_string
    today_roll.html_string = today_html + html
    today_roll.save()
