import binascii
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from security.jwt_gen import JWTEncoder
import time
from telapi.models import Instruction, Task, Ownership, Grant, Access, SensorData, SensorType, FlatOwner, Flat
from .models import Settings_alerts,Settings_forms
from security.permissions import IsIot, IsClient, IsSuperuser, IsOwner
import datetime
from telapi.validations import validate_date, validate_datetime, validate_clientemail, validate_integer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from django.shortcuts import render
from django.contrib.auth import logout as logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.backends import ModelBackend, UserModel
from django.template import loader
from django.http import HttpResponse, Http404
from security.authorization import InstructionAuthorization
from django.db import DatabaseError
from django.db import transaction
from django.contrib.auth.decorators import login_required

# -------show mainpage of owner-----------------

@login_required
def home(request):
    context = {}
    context['msg'] = request.user

    id_flats = []
    flats = []

    for e in FlatOwner.objects.all():
        if e.owner_user.id == request.user.id:
            id_flats.insert(0, e.flat.id)

    for e in Flat.objects.all():
        if e.id in id_flats:
            flats.insert(0, e)

    context['accesos']=Instruction.objects.order_by('-recieved_date')[:2]

    context['flats'] = flats

    template = loader.get_template('owner/home.html')
    return HttpResponse(template.render(context, request))
    
@login_required
def settings(request):
    context = {}
    template = loader.get_template('owner/settings.html')
    return HttpResponse(template.render(context, request))

@login_required
def savesettings_alert(request):
    context = {}
    context['msg'] = request.user
    permission_classes = [IsOwner]

    if request.method == 'POST':
        
        settings_alert = Settings_alerts(
        owner_user=request.user,
        max_temperature=request.POST["max_temperature"],
        min_temperature=request.POST["min_temperature"],
        start_time=request.POST["start_time"],
        end_time=request.POST["end_time"],
        max_capacity=request.POST["max_capacity"],
        listening_time=request.POST["listening_time"])
        settings_alert.save()

        template = loader.get_template('owner/settings.html')
        return HttpResponse(template.render(context, request))

@login_required
def savesettings_form(request):
    context = {}
    context['msg'] = request.user
    permission_classes = [IsOwner]

    if request.method == 'POST':
        
        settings_forms = Settings_forms(
        owner_user=request.user,
        
        )
        settings_alert.save()

        template = loader.get_template('owner/settings.html')
        return HttpResponse(template.render(context, request))

@login_required
def reservation(request):

    id_flats = []
    flats = []

    for e in FlatOwner.objects.all():
        if e.owner_user.id == request.user.id:
            id_flats.insert(0, e.flat.id)

    for e in Flat.objects.all():
        if e.id in id_flats:
            flats.insert(0, e)

    context = {}

    context['flats'] = flats

    template = loader.get_template('owner/reservation.html')
    return HttpResponse(template.render(context, request))
        

@login_required
def logout(request):
    context = {}
    logout(request)
    request.close()
    return render(request, 'owner/logout.html', context)


"""

    for e in SensorData.objects.all()[:2].order_by('recieved_date'):
        if e.flat.id in id_flats:
            sensor.insert(0, e)        

    for e in FlatSensor.objects.all():
        if e.flat.id in id_flats:
            sensor_flats.insert(0, e)

    for e in Instruction.objects.all():
        if e.flat.id in id_flats:
            open_flat=e.__str__     

    context['open_flat'] = open_flat 
    context['sensor_flats'] = sensor_flats  
    context['sensor'] = sensor
    context['flats'] = flats
    context['msg'] = user.username

    template = loader.get_template('owner/ownerpanel.html')
    return HttpResponse(template.render(context, request))"""


# -------show page of the form of owner-----------------
"""
def create_access(request):
    context = {}
    owner = request.session['user']
    owner_object = User.objects.get(username__icontains=owner)
    id_flats = []
    flats = []
    piso_owner = ''
    for e in FlatOwner.objects.all():
        if e.owner_user.id == owner_object.id:
            id_flats.insert(0, e.flat.id)

    for e in Flat.objects.all():
        if e.id in id_flats:
            flats.insert(0, e)

    context['flats'] = flats
    context['msg'] = owner_object
    template = loader.get_template('owner/createaccess.html')
    return HttpResponse(template.render(context, request))"""


# -------createa new access in BBDD-----------------

"""
def new_reservation(request):
    context = {}
    owner = User(owner_object)
    # try:
    usuario = User_App(
        username=request.POST["nombre_usuario"],
        lastname=request.POST["apellidos_usuario"],
        city=request.POST["city"],
        country=request.POST["country"],
        email=request.POST["email"],
        birthdate=request.POST["birthdate"],
        cp=request.POST["cp"],
        nif=request.POST["dni_usuario"],
        phone=request.POST["telefono_usuario"])
    usuario.save()

    newreservation = Reservation(
        owner_id=owner.id,
        user_id=usuario,
        flat_id=request.POST["flats_list"],
        fecha_inicio=request.POST["fecha_inicio"],
        fecha_fin=request.POST["fecha_fin"],
        huespedes_reserva=request.POST["huespedes"])
    newreservation.save()
    return HttpResponseRedirect('panel')"""
