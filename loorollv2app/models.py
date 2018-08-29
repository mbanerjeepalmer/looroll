from django.db import models
from django.contrib.auth.models import User
import datetime

class Roll(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    html_string = models.TextField()

    def __str__(self):
        return str(self.created_date)


# TODO
# class Sheet(models.Model):
#     html_string
#     created date
#     other deets
#     most importantly just make Roll an aggregation of these things with a relationship of some sort


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, blank=True)
    token_type = models.CharField(max_length=255, blank=True)
    expires_at = models.FloatField(blank=True)
    expires_in = models.FloatField(blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True)
    scope = models.CharField(max_length=255, blank=True)
