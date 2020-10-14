from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='superadmin-home'),
    path('logout', auth_views.LogoutView.as_view(template_name=''), name='logout'),  # logout
]
