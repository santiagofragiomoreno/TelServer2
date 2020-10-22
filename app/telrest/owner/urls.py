from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout, name='logout'),
    path('historic_access/', views.historic_access, name='historic_access'),
    path('clean_master/', views.clean_master, name='clean_master'),
    path('reservation/', views.reservation, name='reservation'),
    path('save_reservation/', views.save_reservation, name='save_reservation'),
    path('savesettings_alert/', views.savesettings_alert, name='savesettings_alert'),
    path('savesettings_form/', views.savesettings_form, name='savesettings_form'),
    path('savesettings_ck/', views.savesettings_ck, name='savesettings_ck'),
]
