from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from owner import views as views_owner

urlpatterns = [
    path('panel.ehlock.test/', auth_views.LoginView.as_view(template_name='ownerlog.html'), name='owner_log'),
    path('buscar', views.consulting, name='owner'),

]