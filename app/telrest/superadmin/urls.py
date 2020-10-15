from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='superadmin-home'),
    path('logout', auth_views.LogoutView.as_view(template_name='ownerlog.html'), name='logout'),
    path('altacliente/', views.alta_cliente, name='altacliente'),
    path('altapisos/', views.alta_pisos, name='altapisos'),
    path('errores/', views.errores, name='errores'),
    path('bdowners/', views.bdowners, name='bdowners'),
    path('historial/', views.historial, name='historial'),
]
