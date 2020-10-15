from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('ownerlog/', auth_views.LoginView.as_view(template_name='ownerlog.html'), name='owner_log'),  # Panel.ehlock.com
    path('', auth_views.LoginView.as_view(template_name='ownerlog.html'), name='login'),  # main page?
    path('buscar', views.consulting, name="buscar"),
]