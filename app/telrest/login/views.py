import binascii
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from security.jwt_gen import JWTEncoder
import time
from telapi.models import Instruction, Task, Ownership, Grant, Access, SensorData, SensorType, FlatOwner, Flat
from .models import User_App, Reservation
from security.permissions import IsIot, IsClient, IsSuperuser, IsOwner
import datetime
from telapi.validations import validate_date, validate_datetime, validate_clientemail, validate_integer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import HttpResponse, Http404
from security.authorization import InstructionAuthorization
from django.db import DatabaseError
from django.db import transaction
from django.contrib.auth.decorators import login_required

owner = None
owner_object = None


# Create your views here.
# -------index of log-----------------


def owner_log(request):
    context = {}
    template = loader.get_template('ownerlog.html')
    return HttpResponse(template.render(context, request))


# ---------use for login in BBDD-------------------


def owner_log_info(request):
    context = {
        'ms': '',
        'user': False,
        'super': False,
        'staff': False
    }
    global owner, owner_object
    if request.POST["email"] and request.POST["password"]:
        username = request.POST["email"]
        password = request.POST["password"]
        # filter search in list if exists user with username and password equals at the form
        usuario = User.objects.filter(
            username__icontains=username, password__icontains=password)
        owner_object = User.objects.get(username__icontains=username)
        if usuario:
            owner = request.POST["email"]
            context['msg'] = owner
            context['super'] = owner_object.is_superuser
            context['staff'] = owner_object.is_staff
            template = loader.get_template('ownerpanel.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('ownerlog/')
    else:
        return HttpResponseRedirect('ownerlog/')


# -------show mainpage of owner-----------------



def owner_panel(request):
    context = {}
    context['msg'] = owner
    template = loader.get_template('ownerpanel.html')
    return HttpResponse(template.render(context, request))


# -------show page of the form of owner-----------------


def create_access(request):
    context = {}
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
    template = loader.get_template('createaccess.html')
    return HttpResponse(template.render(context, request))


# -------createa new access in BBDD-----------------


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
    return HttpResponseRedirect('panel')


def administrar(request):
    """ Administration method for super admins """

    context = {
        'users': User_App.objects.all()
    }

    template = loader.get_template('administrar.html')
    return HttpResponse(template.render(context, request))

