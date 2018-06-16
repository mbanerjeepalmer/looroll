from django.db import models
import datetime

class Roll(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    html_string = models.TextField()

    def __str__(self):
        return str(self.created_date)
