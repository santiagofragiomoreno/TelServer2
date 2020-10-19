from django.urls import path, include
from . import views, views_owner

urlpatterns = [
    # ------------------- Test Btns -------------------
    path('stryujk4ijt8p0ni06l916vntlgm72ib8nvj', views.index, name='index'),
    # iot_2
    path('12tcq0tihbld9l9t12f5a8e085qddui9rbs4xwrt', views.main_door_iot2, name='maindoor'),
    path('r5xb259ospdbbqy7ui4hktdks0gnfi7zgzjuggky', views.building_door_iot2, name='buildingdoor'),
    # iot_3
    path('mjnrdahjg0lgtgtd6zh5ha9viipd1s8n0wn', views.main_door_iot3, name='maindoor'),
    path('mjnrdahjg0l6zh5hayytrt9vigm72ib8nvj', views.building_door_iot3, name='buildingdoor'),

    # ------------------- Test Logs -------------------
    path('5hayytrt9vigm72i', views.log_molino, name='logs'),

    # ------------------- App -------------------
    # Activate access code
    path('1y24nmunu7pl5d3krixqp4b4spj54k', views.ActivateAccessCode.as_view(), name='activate_access_code'),
    # Instruction
    path('ot1up02vr1m53kl61bemvfyhs2d2t3', views.InstructionView.as_view(), name='instruction'),

    # ------------------- IoT -------------------
    path('payload', views.Payload.as_view(), name='payload'),

    # ------------------- Owner -------------------
    path('request-client-access', views_owner.RequestClientAccess.as_view(), name='request-client-access'),
    path('flats', views_owner.MyFlats.as_view(), name='flats'),
    path('accesses', views_owner.Accesses.as_view(), name='accesses'),
    # Accesos activos ahora
    # Accesos con pag y search
    # Datos sensores

    # ------------------- Oauth -------------------
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
