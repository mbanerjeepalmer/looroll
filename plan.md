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

**Authentication**
- https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/
- https://docs.djangoproject.com/en/2.0/topics/auth/default/#module-django.contrib.auth.views
- https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html (sort of)


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
