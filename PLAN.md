# Loo Roll - Version 3

# Sunday 28 November 2021
An experience which leaves the person consuming the content feeling better off than when they started.

Overall journey:
- Wake up in the morning. Feel a need for some entertainment, information about the outside world or something mind expanding. (Or have a moment at another time of day)
- See a prompt to open the user interface.
- Consume some content
- Be enriched
- Enhance and repeat

# 29 January 2022
- Tried to get the Django app back working. Seemed like a dead end.
- Tried to rebuild Gmail logic from scratch and build something minimal in an hour. Didn't work.
- Then tried to get the Gmail logic working on its own.
- Tried again with Django. Whitenoise and WSGI errors suggest again that this might be a bad idea.

https://127.0.0.1:8000/auth/complete/google-oauth2/?state=yxSwdzzSpkN9Qxqxm6Mr5jLtKhI9j2&code=4/0AX4XfWg1d_dIUzKQefb3LW6LKnpTp4V_kU-3A1PpchMQMNdClQZueiFOr4c9uFpcpituoQ&scope=https://www.googleapis.com/auth/gmail.modify


# 30 January 2022
- Now gets email IDs, gets their HTML. Most of the time.
- Dealing with the MIME emails has been a challenge. They worked for a good few hours but now don't work again.
- Similarly the few tests I have have been weird.
- Plan for the next steps is:
	- Get the 'daily' run working.
	- Get it dumping JSON files.
	- Then build a static site (effectively) from the JSON files: https://medium.com/swlh/baking-static-sites-with-python-and-jinja-330fe29bbe08

# 2 February 2022
- Now writes

TODO
- [X] Fix side effects from current tests
- [ ] Use a pickled (or other non-API) version of `parsed_email`.
- [ ] Fix duplicate dates in filenames
- [ ] Write HTML files to folder
- [ ] Build static site from folder
- [ ] Tests for 'daily_run'
