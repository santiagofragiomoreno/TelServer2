from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.owner_log, name='owner_log'),  # Panel.ehlock.com , (ownerlog/)
    path('buscar', views.owner_log_info, name='owner'),
    path('panel', views.owner_panel, name='panel'),  # Panel.ehlock.com/owner , (panel)
    path('createaccess', views.create_access, name='createaccess'),
    path('newreservation', views.new_reservation, name='newreservation'),
]