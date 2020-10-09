from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('ownerlog/', views.owner_log, name='owner_log'),#Panel.ehlock.com
    path('buscar', views.owner_log_info, name='owner'),
    path('panel', views.owner_panel, name='panel'),#Panel.ehlock.com/owner
    path('createaccess', views.create_access, name='createaccess'),
    path('newreservation', views.new_reservation, name='newreservation'),
]