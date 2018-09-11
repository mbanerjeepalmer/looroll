"""Pull together the different functions etc and execute."""
import os
import pdb


# TODO See if I can move this elsewhere.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loorollv2.settings.local")
import django
django.setup()
from scripts import gmail_access, write
from loorollv2app.models import UserProfile

# user = os.environ['TEST_EMAIL_ADDRESS']

# token = {
#     'access_token': profile.access_token,
#     'token_type': 'Bearer',
#     'expires_in': 3600,
#     'refresh_token': os.environ['GOOGLE_REFRESH_TOKEN'],
#     'scope': ['https://www.googleapis.com/auth/gmail.modify'],
#     'expires_at': 1533628462.5902889
# }

def main():
    user_profiles = UserProfile.objects.all()
    for profile in user_profiles:
        # pdb.set_trace()
        token = profile.__dict__
        # del token['id'], token['user_id'], token['_state'], token['access_token'], token['token_type'], token['expires_at'], token['expires_in']
        token['client_secret'] = os.environ['GOOGLE_CLIENT_SECRET']
        token['client_id'] = os.environ['GOOGLE_CLIENT_ID']
        client = gmail_access.refresh_access_token(token)
        msg_ids = gmail_access.gmail_query(client, 'me', 'newer_than:1d category:promotions OR label:looroll')
        for msg_id in msg_ids:
            mimedocument = gmail_access.get_email_body(client, 'me', msg_id)
            today_roll = today_or_create_roll(profile.user)
            write.html_to_roll(mimedocument, today_roll, profile.user)
            print(msg_id)
        print ('Done')


if __name__ == "__main__":
    main()
