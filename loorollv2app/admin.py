from django.contrib import admin

# Register your models here.
from .models import Roll, UserProfile

admin.site.register(Roll)
admin.site.register(UserProfile)
