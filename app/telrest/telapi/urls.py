from django.urls import path, include
from . import views

urlpatterns = [
    path('index', views.Index.as_view(), name='index'),
    path('payload', views.Payload.as_view(), name='payload'),
    path('task', views.CreateTask.as_view(), name='task'),
    path('request-client-access', views.RequestClientAccess.as_view(), name='request-client-access'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]