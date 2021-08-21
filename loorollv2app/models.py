from django.db import models
from django.contrib.auth.models import User
import datetime

class Roll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # TODO I think the the null=true is wrong because every Roll needs a user...
    created_date = models.DateTimeField(auto_now_add=True)
    html_string = models.TextField()

    def __str__(self):
        return str(self.created_date)

class Sheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    gmail_id = models.CharField(max_length=255)
    html_string = models.TextField()

    def __str__(self):
        return str(self.created_date)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) #TODO I think the the null=true is wrong because every UserProfile needs a user...
    access_token = models.CharField(max_length=255, blank=True)
    token_type = models.CharField(max_length=255, blank=True)
    expires_at = models.FloatField(blank=True)
    expires_in = models.FloatField(blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True)
    scope = models.CharField(max_length=255, blank=True)
