from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout'),
    path('reservation/', views.reservation, name='reservation'),
    path('savesettings_alert/', views.savesettings_alert, name='savesettings_alert'),
    path('savesettings_form/', views.savesettings_form, name='savesettings_form'),
]
