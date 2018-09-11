"""Take stuff and read or write it to or from the database."""
import django
from loorollv2app.models import Roll
import datetime
from django.core.exceptions import ObjectDoesNotExist


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

def today_or_create_roll(user):
    django.setup()
    today_roll = Roll.objects.filter(user=user).latest(field_name='created_date')
    if not today_roll:
         # TODO handle empty using .exists()
    # except ObjectDoesNotExist:
        t = Roll(html_string='', user=user)
        t.save()
    if today_roll.created_date.date() != datetime.date.today():
        t = Roll(html_string='', user=user)
        t.save()
    return today_roll
   

def html_to_roll(mimedocument, roll, user):
    # TODO Do this by email ID or something clever, email by email
    # TODO Also mark processed emails as read an apply the 'looroll' label to them
    html = mimedocument.get_body().get_content()
    # TODO Better option should be the F thing and/or Concat:
    # https://docs.djangoproject.com/en/2.0/ref/models/database-functions/#django.db.models.functions.Concat
    # https://docs.djangoproject.com/en/2.0/ref/models/expressions/#django.db.models.F
    # https://docs.djangoproject.com/en/2.0/topics/db/queries/#topics-db-queries-update
    django.setup()
    today_roll = Roll.objects.filter(user=user).latest(field_name='created_date')
    today_roll.html_string += html
    today_roll.save()
