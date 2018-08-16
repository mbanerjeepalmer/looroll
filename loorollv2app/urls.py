from django.urls import include, path
from django.contrib.auth import views, urls
from . import views

urlpatterns = [
    path('', views.roll, name='roll'),
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
]
