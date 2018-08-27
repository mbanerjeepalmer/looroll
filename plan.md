# Plan

- Set up Django project
- Create models:
  - Columns: Date created, HTML string
- Create views:
  - Only one view
  - Find most recent HTML string (go into DB, find max date/sort by date/something, pull the HTML string column)
  - Send HTML string ~~as context to the template~~ as whole page
- Template: ~~literally just the HTML string~~ none
- Password:
  - Add a password to this page
- Script:
  - Set up new criterion for pulling in an email (this could actually just be to apply a label within Gmail itself)
  - Connect to DB and make a new entry, with the HTML string
- Deploy to Python Anywhere


# Resources
## Tutorials
- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment
- https://tutorial.djangogirls.org/en/django_start_project/
- https://hackernoon.com/0-100-in-django-starting-an-app-the-right-way-badd141ef439
- https://peeomid.com/blog/2018-01-26-what-i-wish-i-knew-when-i-started-django-development-2018/
- https://docs.djangoproject.com/en/2.0/intro/tutorial01/
- https://jeffknupp.com/blog/2013/12/18/starting-a-django-16-project-the-right-way/
- https://medium.com/@djstein/modern-django-part-0-introduction-and-initial-setup-657df48f08f8 (haven't read)

## Books
- https://books.agiliq.com/en/latest/

### Authentication
- https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/
- https://docs.djangoproject.com/en/2.0/topics/auth/default/#module-django.contrib.auth.views
- https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html (sort of)
- https://djangobook.com/user-authentication-django/

### SSL/HTTPS
- https://www.petercuret.com/how-ssl-encrypt-your-django-heroku-projects-free-lets-encrypt/
- 

### OAuth
For the deprecated client
- https://developers.google.com/api-client-library/python/auth/web-app
- https://developers.google.com/api-client-library/python/guide/django
- https://developers.google.com/api-client-library/python/guide/aaa_oauth#OAuth2WebServerFlow
- https://github.com/google/oauth2client/tree/master/samples/django

New options
- http://google-auth-oauthlib.readthedocs.io/en/latest/
- https://requests-oauthlib.readthedocs.io/en/latest/
- Errr https://github.com/jazzband/django-oauth-toolkit
- http://media.readthedocs.org/pdf/python-social-auth/latest/python-social-auth.pdf
- https://goodcode.io/static/media/OAuth2-edited.pdf
- https://gist.github.com/ib-lundgren/6507798

Safe keeping
- https://gist.github.com/EugeneLiang/4bde544cd9b572142a62#file-apiauth-py

## Tools
### Prettification and conversion
- https://github.com/thespacedoctor/polyglot
- https://pandoc.org


# Diary
## 3 June
Got started. Took ages.
Can send HTML string `<html><body>Imagine this was a huge email.</body></html>`

## 4 June
Started at 10ish.
23:49: Views, model and admin done.

### TO DO
Password protection
Deployment
Connect script

For all three I should just check what I did with Rango.

## 14 June
Started around 10.
23:22 Sorted out the script so that it can alter Django from outside the application.

### TO DO
Now need to do the authentication. This means transferring over to the template (rather than returning the direct response), changing the view and also the urlconf. More to it than I remembered. Rango has a decent amount on it. Can also check the Mozilla tutorial.


## 15 June
7ish to 7:50. Really need to work out how to log time and powershell better.
At great length realised I could just block it for everyone and then only allow user registration from admin screens.

### TO DO
Deploy!

## 16 June
Spent a shit ton of time on it today. Essentially 11 - 11 while watching the world cup.
Deployed and made it production-ready using environment variables. (Is that bad? Should I be using something else?)
Now need to plan what happens next. I think it's either how the emails are displayed or from where I get them.

### TO DO
It's probably more useful to start with where I get them from? Otherwise it's making an insufficent number of emails more pretty. Later I also need to sort the user question (i.e. ouath2).

On making it more pretty I need someone else's way of making it look like Pocket

What are the criteria?
How should it be stored? A series of queries? That then adds each email ID to the DB? And ensure there are no duplicates.

pseudocode
make a new session with a timestamp, log that in the database
for query in queries
  give me email message ids
store the message ids in the database
  if there's a duplicate, skip it
for each message id, store the html
for a session id make an html file/field
  for each bit of html that matches that session id, append the html for that message to the end of the field

model:
  timestamp created
  session number
  query number (?)
  gmail message id
  message html

#### TO DO TO DO
- Split script into scripts to make it usable
- Do the stuff above

## 17 June
09:30 (or earlier)
Notes
Input should include 'paste a URL'.

Finish:
22:10
Big day. Not loads achieved.
Perhaps I should set a pomodoro style reminder to note progress every half hour.

Finished with the following message `OSError: [Errno 101] Network is unreachable`
Feels like time to shift to Heroku (or digital ocean?). Either that or work out how to make Gmail API client work via a proxy.

It did work earlier though, which is weird.

## TO DO
Error handling.
Absolute versus relative paths.
Line splits are a bit concerning...
And then the rest of the TODOs.

## 20 June

## 21 June
- Didn't do anything about static files: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment#Serving_static_files_in_production
Lost access to looroll heroku


## 26 June
- It's fucking deprecated! https://oauth2client.readthedocs.io/en/latest/index.html
- Use google-auth and/or  authlub instead?!

### 2-3 July
- Tried requests-oauthlib but now on python-social-auth

10:20 3 July
- Done most settings changes I think.
- Looks like the URLs will autoresolve to /login ?
  - Turns out it needed `from django.contrib.auth import views` in the main urls.py

### 5 July
- These two tutorials were for a different version to the one I'm using...
  - https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html
  - https://fosstack.com/how-to-add-google-authentication-in-django/

### 4 August
- OAuth2
  - !(2018-08-04 22:09)
      - Get the access token
          - Follow the correct steps for Django. Certainly by looking at GitHub or something.
          - As a minimum I'm more comfortable with the constituent steps
      - Use it to access protected resources
          - Requests library as normal? Grab the `access_token` from the DB?
          - The docs are suggesting no, use the object instead...
          - Success: add it as a header.
      - Refresh token
          - Specified here: https://developers.google.com/identity/protocols/OAuth2WebServer
          - Probably. Only if I look at the HTTP version.

### 5 August
-
-

### 7 August
- TODO
  - **Step 4: Handle the OAuth 2.0 server response:** Carefully consider whether you want to send authorization credentials to all resources on that page (especially third-party scripts such as social plugins and analytics). To avoid this issue, we recommend that the server first handle the request, then redirect to another URL that doesn't include the response parameters.
- Sort out refresh token
  - Got one this morning
  - Use it now (Success: 22:39)

-TODO
  - Rewrite everything that interacts with Gmail
    - Rewritten access (Success: 23:48)
    - TODO Rewrite query
  - TODO Get the rest of Django OAuth working.
    - Note the 'Server response' thing above
    - ORM
  - TODO Set this up for users
    - User creates account
    - User links that account to Google account
    - Application grabs and sends specific emails to user
      - Which emails?
        - User chooses
        - Looks useful to filter once chosen https://developers.google.com/gmail/api/guides/filter_settings
      - How to grab and send?
        - Schedule script on Heroku
          - For loop for each user?
        - Sending is email plus site (behind login page)
          - Email not too tricky
          - Site need to make sure adding to DB and then displaying in view works properly


### 8 August
- What's the Django side of this? (Most of what's noted above relates to the Gmail API side)
  - I suppose the flow is:
    (1) Login page
      View supplies the auth url to the user
        View generates the URL using requests-oauthlib OAuthSession from the gmail-access module
        View passes that url to the template in a context dict
      Template displays it
        Template displays the authorisation URL if the user is logged in
    (2) Callback page
      View and template exist to be redirected to
        The URL is registered with Google
        The template may or may not be necessary, depending on whether the user stays there or not.
      View pulls in the URL from the page
        Is this a separate view? Or can I differentiate based on GET / POST?
        View grabs URL the user is on and stores in a variable
      View uses the response URL to send the request to the server, fetch the tokens and save them to the DB.
        View uses the OAuthSession client to fetch the tokens in the background
        View has access to the User model in the DB and saves the fields of the token (access, refresh, expires etc.) in columns
      Redirect to another page maybe?
        Is this necessary? Or just say 'Go to home to see today's loo roll'.

TODO  Template + View for standard auth
        See Rango
TODO How does it handle state?
TODO (long grass): remove the need for standard Django login altogether. Something like django simple social auth might provide guidance on how to do so.

### 11 August
- Sort of worked out the view.
  - But HTTPS is going to be necessary
  - Look for an example
- User model

### 14 August
- Change of plan: do something minimal for the moment so I'm actually getting this
  - Use plain auth token etc. from Gmail Access module
  - Sort proper auth and DB (i.e. other users) later
- How would I do this?
- TODO
  - Saving HTML string to Django DB
    - Ensure it's being appended
  - Push to Heroku and survey the damage...


### 18 August
- We are cooking! It works. I can:
  - Ask Heroku to run `script.py` and this will grab the emails with the 'looroll' label received within the last day and display them as one huge block of HTML.
- On the pseudo roadmap
  - Users/auth
    - It's not clear that this works *at all* to be honest. I can't get in on mobile.
    - OAuth2 wise, I need to set up HTTPS.
  - Prettification
    - Pandoc via Python
    - Any other options? Like Firefox and other readability options.
  - Sourcing
    - Inbox analytics
    - Set filters, whether from analytics or manually
  - Further functionality
    - Pocket API
    -
- So:
  (1) Auth
  (2) Set filters
  (3) Everything else
Auth: Makes sense to kill two birds with one stone and finish the Django tutorial again.

### 26 August
- Finally got through the official tutorial again. And then spent half an hour on an auth tutorial.

TODO
- Get through the rest of the other auth tutorial.
- Get back to building. Plus maybe build the spotify thing.
- Within (3) above, one big thing might be SSL.

### 27 August
- Get through the rest of the other auth tutorial.
  - Done that sort of. Although there isn't a registration thing at the moment...
- Get back to building. Plus maybe build the spotify thing.
- Within (3) above, one big thing might be SSL.

Doing
-

------------------------
Putting here for safe storage:
```python
  def get_events():
      r = requests.get('http://www.lse.ac.uk/Events/Search-Events')
      soup = BeautifulSoup(r.text, 'html.parser')
      event_results = soup.find(class_='largeList').get_text()
      with open(filename, 'w', encoding="utf-8") as outfile:
          outfile.write(event_results)
      print ('Events saved.')
      # events =
      # for e in events:
      # also put in the html2text

  def plain_text_parser():
      pass
      #html2text goes here
```
