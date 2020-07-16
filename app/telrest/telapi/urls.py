from django.urls import path, include
from . import views

urlpatterns = [
    # ------------------- Test Btns -------------------
    path('stryujk4ijt8p0ni06l916vntlgm72ib8nvj', views.index, name='index'),
    path('mjnrdahjg0lgtgtd6zh5ha9viipd1s8n0wn', views.main_door, name='maindoor'),
    path('mjnrdahjg0l6zh5hayytrt9vigm72ib8nvj', views.building_door, name='buildingdoor'),

    # ------------------- App -------------------
    # Activate access code
    path('1y24nmunu7pl5d3krixqp4b4spj54k', views.ActivateAccessCode.as_view(), name='activate_access_code'),
    # Instruction
    path('ot1up02vr1m53kl61bemvfyhs2d2t3', views.InstructionView.as_view(), name='instruction'),

    # ------------------- IoT -------------------
    path('payload', views.Payload.as_view(), name='payload'),

    # ------------------- Owner -------------------
    path('request-client-access', views.RequestClientAccess.as_view(), name='request-client-access'),

    # ------------------- Oauth -------------------
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]