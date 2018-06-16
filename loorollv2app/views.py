from django.http import HttpResponse
from loorollv2app.models import Roll
from django.contrib.auth.decorators import login_required

@login_required
def roll(request):
    html = Roll.objects.latest(field_name='created_date').html_string
    # html = "<html><body>Imagine this was a huge email.</body></html>"
    return HttpResponse(html)
