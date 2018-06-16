from django.urls import path
from django.contrib.auth import views, urls
from . import views

urlpatterns = [
    path('', views.roll, name='roll'),
]
