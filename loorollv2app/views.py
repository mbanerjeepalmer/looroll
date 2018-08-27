from django.http import HttpResponse
from loorollv2app.models import Roll
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from requests_oauthlib import OAuth2Session
import os

scope = 'https://www.googleapis.com/auth/gmail.modify'
redirect_uri = 'https://loorolls.herokuapp.com/rolls/callback/'
authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
access_type = 'offline'
prompt = 'select_account'
token_url = 'https://www.googleapis.com/oauth2/v4/token'

@login_required
def roll(request):
    html = Roll.objects.latest(field_name='created_date').html_string
    return HttpResponse(html)


@login_required
def home(request):
    return render(request, 'rolls/home.html')

def login(request):
    client_id = os.environ['GOOGLE_CLIENT_ID']
    client_secret = os.environ['GOOGLE_CLIENT_SECRET']
    client = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = client.authorization_url(authorization_base_url, access_type='offline', prompt='select_account')
    context_dict = {'authorization_url': authorization_url}
    return render(request, 'registration/login.html', context_dict)

def callback(request):
    client_id = os.environ['GOOGLE_CLIENT_ID']
    authorization_response = request.build_absolute_uri()
    client = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    token = client.fetch_token('https://accounts.google.com/o/oauth2/token', authorization_response=authorization_response, client_secret=client_secret)
    return HttpResponse(token)    # TODO Check refresh token in response and change prompt to 'consent' if not
