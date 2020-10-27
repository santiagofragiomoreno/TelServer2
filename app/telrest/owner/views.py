import binascii
import os
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.db import IntegrityError, transaction
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from security.jwt_gen import JWTEncoder
import time
from telapi.models import Instruction, Task, Ownership, Grant, Access, SensorData, SensorType, FlatOwner, Flat, Flat_Owner_Access,Client
from .models import Settings_alerts,Settings_forms,Payments
from telapi.models import Reservation as model_reservation
from security.permissions import IsIot, IsClient, IsSuperuser, IsOwner
import datetime
from telapi.validations import validate_date, validate_datetime, validate_clientemail, validate_integer
from django.contrib.auth.models import User,Group
from .fomrs import Settings_alerts as alerts
from django.db import transaction
from django.contrib import messages
from .fomrs import Settings_forms as form_form
from .fomrs import Settings_checkout as ck
from .fomrs import Reservation as form_reservation
from .fomrs import Client as form_client
from .fomrs import Filter,Observation
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from django.shortcuts import render
from django.contrib.auth import logout as logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import HttpResponse, Http404
from security.authorization import InstructionAuthorization
from django.db import DatabaseError
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import EmailMessage

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
            id_flats.append(e.flat.id)

    for e in Flat.objects.all():
        if e.id in id_flats:
            flats.append(e)

    context['accesos']=Instruction.objects.order_by('-recieved_date')[:2]

    context['flats'] = flats

    template = loader.get_template('owner/home.html')
    return HttpResponse(template.render(context, request))

#------------formularios seguros

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
            id_flats.append(e.flat.id)

    for e in Flat.objects.all():
        if e.id in id_flats:
            flats.append(e)

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
#@transaction.atomic
def savesettings_alert(request):
    context = {}
    context['msg'] = request.user
    try:
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
    except IntegrityError:
        settings_alert = Settings_alerts.objects.get(owner_user=request.user)
        settings_alert.max_temperature=form.cleaned_data.get('max_temperature')
        settings_alert.min_temperature=form.cleaned_data.get('min_temperature')
        settings_alert.start_time=form.cleaned_data.get('start_time')
        settings_alert.end_time=form.cleaned_data.get('end_time')
        settings_alert.max_capacity=form.cleaned_data.get('max_capacity')
        settings_alert.listening_time=form.cleaned_data.get('listening_time')          
        settings_alert.save()

    template = loader.get_template('owner/settings.html')
    return HttpResponse(template.render(context, request))

@login_required

def savesettings_form(request):
    context = {}
    context['msg'] = request.user

    try:
        if request.method == 'POST':
            form=form_form(request.POST)            
        if form.is_valid():
            settings_forms = Settings_forms(
            owner_user=request.user,
            is_lastname=form.cleaned_data.get('is_lastname'),
            is_phone=form.cleaned_data.get('is_phone'),
            is_city=form.cleaned_data.get('is_city'),
            is_birthdate=form.cleaned_data.get('is_birthdate'),
            is_import=form.cleaned_data.get('is_import'),
            is_origin=form.cleaned_data.get('is_origin'),
            is_code=form.cleaned_data.get('is_code'),
            is_capacity=form.cleaned_data.get('is_capacity'),
            is_cancelation=form.cleaned_data.get('is_cancelation'),
            is_observation=form.cleaned_data.get('is_observation'),
            is_pay=form.cleaned_data.get('is_pay'),
            )
            settings_forms.save()

    except IntegrityError:
        settings_forms = Settings_forms.objects.get(owner_user=request.user)
        settings_forms.is_lastname=form.cleaned_data.get('is_lastname')
        settings_forms.is_phone=form.cleaned_data.get('is_phone')
        settings_forms.is_city=form.cleaned_data.get('is_city')
        settings_forms.is_birthdate=form.cleaned_data.get('is_birthdate')
        settings_forms.is_import=form.cleaned_data.get('is_import')
        settings_forms.is_origin=form.cleaned_data.get('is_origin')
        settings_forms.is_code=form.cleaned_data.get('is_code')
        settings_forms.is_capacity=form.cleaned_data.get('is_capacity')
        settings_forms.is_cancelation=form.cleaned_data.get('is_cancelation')
        settings_forms.is_observation=form.cleaned_data.get('is_observation')
        settings_forms.is_pay=form.cleaned_data.get('is_pay')          
        settings_forms.save()
    
    template = loader.get_template('owner/settings.html')
    return HttpResponse(template.render(context, request))

@login_required
def savesettings_ck(request):
    context = {}
    context['msg'] = request.user
    permission_classes = [IsOwner]

    try:
        if request.method == 'POST':
            form=ck(request.POST)            
            if form.is_valid():
                payments = Payments(
                owner_user=request.user,
                price_time=form.cleaned_data.get('price_time'),
                time_price=form.cleaned_data.get('time_price'),
                )
            payments.save()

    except IntegrityError:
        payments = Payments.objects.get(owner_user=request.user)
        payments.price_time=form.cleaned_data.get('price_time')
        payments.time_price=form.cleaned_data.get('time_price')
        payments.save()

    template = loader.get_template('owner/settings.html')
    return HttpResponse(template.render(context, request))

@login_required
def reservation(request):
    context = {}
    context['msg'] = request.user
    id_flats = []
    flats = []

    context = {
                    'reservation': {
                        'reserv': {'form': form_reservation},
                        'client': {'form': form_client},
                    }
                }
    
    for e in FlatOwner.objects.all():
        if e.owner_user.id == request.user.id:
            id_flats.append(e.flat.id)

    for e in Flat.objects.all():
        if e.id in id_flats:
            flats.append(e)

    context['flats'] = flats
    try:
        settings_forms = Settings_forms.objects.get(owner_user=request.user)
        context['forms'] = settings_forms
    except 	ObjectDoesNotExist:

        settings_forms = Settings_forms(
            owner_user=request.user,
            is_lastname=True,
            is_phone=True,
            is_city=True,
            is_birthdate=True,
            is_import=True,
            is_origin=True,
            is_code=True,
            is_capacity=True,
            is_cancelation=True,
            is_observation=True,
            is_pay=True,
            )

        settings_forms.save()
        settings_forms = Settings_forms.objects.get(owner_user=request.user)
        context['forms'] = settings_forms

    template = loader.get_template('owner/reservation.html')
    return HttpResponse(template.render(context, request))


@login_required
def save_reservation(request):

    temp={}
    context = {}
    context['msg'] = request.user
    try:
        if request.method == 'POST':
            form=form_client(request.POST)            
            if form.is_valid():
                new_client = User.objects.create_user(form.cleaned_data.get('name'), form.cleaned_data.get('email'), 'default')
                new_client.save()

                # añado el cliente al grupo de clientes
                group_client = Group.objects.get(name='Client')
                group_client.user_set.add(new_client)
                    
                client = Client(
                        auth_id=new_client.id,
                        name = form.cleaned_data.get('name'),
                        lastname = form.cleaned_data.get('lastname'),
                        email = form.cleaned_data.get('email'),
                        dni = form.cleaned_data.get('dni'),
                        birthdate = request.POST["birthdate"],
                        tlf = form.cleaned_data.get('tlf'),
                        direction = form.cleaned_data.get('direction'),
                        city = form.cleaned_data.get('city'),
                        country = form.cleaned_data.get('country'),
                        cp = form.cleaned_data.get('cp'),
                    )
                client.save()

            reservation = model_reservation(
                owner_user=request.user,
                client=client,
                flat_id = request.POST["flat_select"],
                start_time = request.POST["start_time"],
                end_time = request.POST["end_time"],
                guest = form.cleaned_data.get('guest'),
                import_price = form.cleaned_data.get('import_price'),
                cancelation = form.cleaned_data.get('cancelation'),
                origin = form.cleaned_data.get('origin'),
                code = form.cleaned_data.get('code'),
                observation = form.cleaned_data.get('observation'),
                )                
            reservation.save()
            #TODO es necesario que cuando se suba el codigo se descomente y se configura para enviar correos
            """subject="Nueva reserva por parte de " + request.user.username
                messages="Se ha creado una reserva para " + form.cleaned_data.get('name') + " con fecha del " + request.POST["start_time"] + " al " + request.POST["end_time"]

                msg = EmailMessage(subject,messages, to=['romanclementejurado@gmail.com'])
                msg.send()"""

    except IntegrityError:
        # """payments = Payments.objects.get(owner_user=request.user)
        """payments.price_time=form.cleaned_data.get('price_time')
        payments.time_price=form.cleaned_data.get('time_price')
        payments.save()"""

    template = loader.get_template('owner/home.html')
    return HttpResponse(template.render(context, request))


@login_required
def historic_access(request):
    busqueda=[]
    context = {}
    context = {
                'filter': {
                    'flter': {'form': Filter},
                }
            }
    if request.method == 'POST':
        context['msg'] = request.user
        try:
            if request.POST["search"] is None:
                form=Filter(request.POST) 
                if form.is_valid():   
                    selected = form.cleaned_data.get("NUMS")
                    context['accesos']=Flat_Owner_Access.objects.order_by(selected)
            else:
                #or e.auth_user.phone == request.POST["search"]
                for e in Flat_Owner_Access.objects.all():
                    if e.flat.name.lower() == request.POST["search"].lower() or e.auth_user.username.lower() == request.POST["search"].lower() or e.auth_user.last_name.lower() == request.POST["search"].lower():
                        busqueda.append(e)
                context['accesos']=busqueda
        except MultiValueDictKeyError:
            form=Filter(request.POST) 
            if form.is_valid():
                for e in Flat_Owner_Access.objects.all():
                    if e.auth_user.id == request.user.id:
                        busqueda.append(e)
                    selected = form.cleaned_data.get("NUMS")
                    context['accesos']= busqueda
    else:
        context['msg'] = request.user
        context['accesos']=Flat_Owner_Access.objects.all()

    template = loader.get_template('owner/historic_access.html')
    return HttpResponse(template.render(context, request))


@login_required
def edit_access(request):
    context = {}
    context = {
                    'obs': {
                        'observation': {'form': Observation},
                    }
                }
    if request.method == 'POST':
        
        try:
            settings_forms = Settings_forms.objects.get(owner_user=request.user)
            context['forms'] = settings_forms
        except 	ObjectDoesNotExist:

            settings_forms = Settings_forms(
                owner_user=request.user,
                is_lastname=True,
                is_phone=True,
                is_city=True,
                is_birthdate=True,
                is_import=True,
                is_origin=True,
                is_code=True,
                is_capacity=True,
                is_cancelation=True,
                is_observation=True,
                is_pay=True,
                )

            settings_forms.save()
            settings_forms = Settings_forms.objects.get(owner_user=request.user)
            context['forms'] = settings_forms

        

        if request.POST["option"] == '1':

            flat_owner = Flat_Owner_Access.objects.get(pk=request.POST["item"])
            reservation= model_reservation.objects.get(pk=flat_owner.reservation.id)
            context['reservation']=reservation
            context['flat_owner']=flat_owner
            context['type']='1'

        elif request.POST["option"] == '2':

            flat_owner = Flat_Owner_Access.objects.get(pk=request.POST["item"])
            reservation= model_reservation.objects.get(pk=flat_owner.reservation.id)
            template = loader.get_template('owner/historic_access.html')
            return HttpResponse(template.render(context, request))

        else:

            flat_owner = Flat_Owner_Access.objects.get(pk=request.POST["item"])
            reservation= model_reservation.objects.get(pk=flat_owner.reservation.id)
            context['reservation']=reservation
            context['flat_owner']=flat_owner
            context['type']='2'


    template = loader.get_template('owner/edit_access.html')
    return HttpResponse(template.render(context, request))


@login_required
def logout(request):
    context = {}
    logout(request)
    request.close()
    return render(request, 'owner/logout.html', context)

