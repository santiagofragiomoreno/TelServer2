from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
<<<<<<< HEAD
    path('', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
=======
    path('', views.home, name='owner-home'),
>>>>>>> home
    #path('Panel.ehlock.com/access', views.create_access, name='access'),  
]

#
#
#path('newreservation', views.new_reservation, name='newreservation'),
# path('logout', auth_views.LogoutView.as_view(template_name='ownerlog.html'), name='logout'),  # logout
#path('administrar', views.administrar, name='administrar'),
