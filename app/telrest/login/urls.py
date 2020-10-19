from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view, name='login'),
]