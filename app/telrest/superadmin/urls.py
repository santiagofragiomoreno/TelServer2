from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='superadmin-home'),
    path('logout', views.logout_view, name='logout'),
    path('altacliente/', views.alta_cliente, name='altacliente'),
    path('altapisos/', views.alta_pisos, name='altapisos'),
    path('errores/', views.errores, name='errores'),
    path('bdowners/', views.bdowners, name='bdowners'),
    path('ajustes/', views.ajustes, name='ajustes'),
    path('altadispositivo/', views.alta_dispositivo, name='altadispositivo'),
]
