from django.http import HttpResponse
from loorollv2app.models import Roll, UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from requests_oauthlib import OAuth2Session
import os
import traceback
from django.core.exceptions import ObjectDoesNotExist

scope = 'https://www.googleapis.com/auth/gmail.modify'
redirect_uri = 'https://loorolls.herokuapp.com/rolls/callback/'
authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
access_type = 'offline'
prompt = 'consent'
token_url = 'https://www.googleapis.com/oauth2/v4/token'


@login_required
def roll(request):
    user = request.user
    try:
        # TODO obviously need to be storing these separately and then displaying then showing each in an iframe
        # But ultimately I should also be formatting each one so the iframe isn't necessary
        html = Roll.objects.filter(user=user).latest(field_name='created_date').html_string
        return HttpResponse(html)
    except ObjectDoesNotExist:
        return HttpResponse("You don't have any loo roll")


@login_required
def login(request):
    # TODO merge this with the built in login view
    client_id = os.environ['GOOGLE_CLIENT_ID']
    client_secret = os.environ['GOOGLE_CLIENT_SECRET']
    client = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = client.authorization_url(authorization_base_url, access_type='offline', prompt='select_account')
    context_dict = {'authorization_url': authorization_url}
    return render(request, 'registration/login.html', context_dict)


def callback(request):
    # TODO this whole thing is a bit messy and doesn't check state
    try:
        user = request.user
        client_id = os.environ['GOOGLE_CLIENT_ID']
        client_secret = os.environ['GOOGLE_CLIENT_SECRET']
        authorization_response = request.build_absolute_uri()
        client = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
        token = client.fetch_token('https://accounts.google.com/o/oauth2/token', authorization_response=authorization_response, client_secret=client_secret)
        UserProfile.objects.update_or_create(defaults=token, user=user)
        return redirect('https://loorolls.herokuapp.com/rolls/')  # TODO Check refresh token in response and change prompt to 'consent' if not. Right now I'm just hardcoding consent. Plus this redicrect is probably bad.
    except Exception as e:
        #TODO this is bad
        error_message = str(e) + traceback.format_exc()
        return HttpResponse(error_message)
