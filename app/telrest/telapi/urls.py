from django.urls import path, include
from . import views

urlpatterns = [
    # test btns
    path('stryujk4ijt8p0ni06l916vntlgm72ib8nvj', views.index, name='index'),
    path('mjnrdahjg0lgtgtd6zh5ha9viipd1s8n0wn', views.main_door, name='maindoor'),
    path('mjnrdahjg0l6zh5hayytrt9vigm72ib8nvj', views.building_door, name='buildingdoor'),


    path('payload', views.Payload.as_view(), name='payload'),
    path('request-client-access', views.RequestClientAccess.as_view(), name='request-client-access'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]