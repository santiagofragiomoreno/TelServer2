from django.urls import path, include
from . import views

urlpatterns = [
    path('index', views.Index.as_view(), name='index'),
    path('payload', views.Payload.as_view(), name='payload'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]