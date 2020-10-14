from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('ownerlog/', auth_views.LoginView.as_view(template_name='ownerlog.html'), name='owner_log'),  # Panel.ehlock.com
    path('buscar', views.owner_log_info, name='owner'),
    path('panel', views.owner_panel, name='panel'),  # Panel.ehlock.com/owner
    path('createaccess', views.create_access, name='createaccess'),
    path('newreservation', views.new_reservation, name='newreservation'),
    path('logout', auth_views.LogoutView.as_view(template_name='ownerlog.html'), name='logout'),  # logout
    path('administrar', views.administrar, name='administrar'),

]