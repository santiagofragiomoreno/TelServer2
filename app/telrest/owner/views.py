import binascii
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from security.jwt_gen import JWTEncoder
import time
from telapi.models import Instruction, Task, Ownership, Grant, Access, SensorData, SensorType, FlatOwner, Flat
from .models import Settings_alerts,Settings_forms,Payments
from security.permissions import IsIot, IsClient, IsSuperuser, IsOwner
import datetime
from telapi.validations import validate_date, validate_datetime, validate_clientemail, validate_integer
from django.contrib.auth.models import User
from .fomrs import Settings_alerts as alerts
from .fomrs import Settings_forms as form_form
from .fomrs import Settings_checkout as ck
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

#-----TODO terminar con tablas que hacen falta y darle un poco de estilo-----------
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

#------------formularios seguros

@login_required
def historic_access(request):
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

    context['accesos']=Instruction.objects.order_by('-recieved_date')

    context['flats'] = flats
    template = loader.get_template('owner/historic_access.html')
    return HttpResponse(template.render(context, request))

@login_required
def clean_master(request):
    context = {}
    context['msg'] = request.user
    accesos={}
    accesos=Instruction.objects.order_by('-recieved_date')[:2]

    id_flats = []
    flats = []
    for e in FlatOwner.objects.all():
        if e.owner_user.id == request.user.id:
            id_flats.insert(0, e.flat.id)

    for e in Flat.objects.all():
        if e.id in id_flats:
            flats.insert(0, e)

    context['flats'] = flats
    context['accesos']=accesos
    context['tiempo']= accesos[0].recieved_date - accesos[1].recieved_date 

    template = loader.get_template('owner/clean_master.html')
    return HttpResponse(template.render(context, request))

@login_required
def settings(request):
    context = {}
    context['msg'] = request.user
    context = {
                'settings': {
                    'alerts': {'form': alerts},
                    'forms': {'form': form_form},
                    'checkout': {'form': ck},
                }
            }
    template = loader.get_template('owner/settings.html')
    return HttpResponse(template.render(context, request))

@login_required
def savesettings_alert(request):
    context = {}

    if request.method == 'POST':
        form=alerts(request.POST)            
        if form.is_valid():
            settings_alert = Settings_alerts(
                owner_user=request.user,
                max_temperature=form.cleaned_data.get('max_temperature'),
                min_temperature=form.cleaned_data.get('min_temperature'),
                start_time=form.cleaned_data.get('start_time'),
                end_time=form.cleaned_data.get('end_time'),
                max_capacity=form.cleaned_data.get('max_capacity'),
                listening_time=form.cleaned_data.get('listening_time'),
            )
            settings_alert.save()
    template = loader.get_template('owner/home.html')
    return HttpResponse(template.render(context, request))

@login_required
def savesettings_form(request):
    context = {}
    context['msg'] = request.user
    permission_classes = [IsOwner]

    if request.method == 'POST':
        form=form_form(request.POST)            
        if form.is_valid():
            settings_forms = Settings_forms(
            owner_user=request.user,
            is_lastname=form.cleaned_data.get('is_lastname'),
            is_phone=form.cleaned_data.get('is_phone'),
            is_city=form.cleaned_data.get('is_city'),
            is_import=form.cleaned_data.get('is_import'),
            is_origin=form.cleaned_data.get('is_origin'),
            is_code=form.cleaned_data.get('is_code'),
            #is_capacity=form.cleaned_data.get('is_capacity'),
            is_cancelation=form.cleaned_data.get('is_cancelation'),
            is_observation=form.cleaned_data.get('is_observation'),
            is_pay=form.cleaned_data.get('is_pay'),
            )

        settings_forms.save()

        template = loader.get_template('owner/home.html')
        return HttpResponse(template.render(context, request))

@login_required
def savesettings_ck(request):
    context = {}
    context['msg'] = request.user
    permission_classes = [IsOwner]

    if request.method == 'POST':
        form=ck(request.POST)            
        if form.is_valid():
            payments = Payments(
            owner_user=request.user,
            price_time=form.cleaned_data.get('price_time'),
            time_price=form.cleaned_data.get('time_price'),
            )
        payments.save()

        template = loader.get_template('owner/home.html')
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
def save_reservation(request):
    context = {}
    context['msg'] = request.user

    if request.method == 'POST':
        form=ck(request.POST)            
        if form.is_valid():
            access = Access(
            )
            access.save()

        template = loader.get_template('owner/home.html')
        return HttpResponse(template.render(context, request))

@login_required
def logout(request):
    context = {}
    logout(request)
    request.close()
    return render(request, 'owner/logout.html', context)

