import binascii
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from security.jwt_gen import JWTEncoder
import time
from telapi.models import Instruction, Task, Ownership, Grant, Access, SensorData, SensorType,FlatOwner,Flat
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
    context = {}
    context['msg'] = ''
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
    owner_object = User.objects.get(username__icontains=owner)
    for e in FlatOwner.objects.all():
        piso_owner=e
    #b = FlatOwner(owner_user_id=owner_object)
    #b.objects.get()
    #piso_owner = [owner_user_id__owner_object.id]
    #piso_owner=FlatOwner.objects.filter(owner_user__contains=7)
    context = {}
    context['msg'] =  piso_owner
    template = loader.get_template('createaccess.html')
    return HttpResponse(template.render(context, request))

# -------createa new access in BBDD-----------------


def new_reservation(request):
    context = {}
    try:
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
        return HttpResponseRedirect('panel')
        """newreservation = Reservation(
            owner_id=owner_object,
            user_id=usuario,
            piso_owner="PISO PRUEBA",
            fecha_inicio=request.POST["fecha_inicio"],
            fecha_fin=request.POST["fecha_fin"],
            huespedes=request.POST["huespedes"])
        newreservation.save()"""
        
    except DatabaseError as saveException:
        try:
            transaction.rollback()
            context['msg'] = 'No se pudo realizar esa insercion en la BBDD'
            template = loader.get_template('ownerpanel.html')
            return HttpResponse(template.render(context, request))
        except Exception as rollbackException:
            context = 'No se pudo realizar rollback'
            return HttpResponse(context)

    return HttpResponse(context)

    """
def comprobacion(request):
    if request.POST["nombre_usuario"] and request.POST["apellidos_usuario"] and  request.POST["dni_usuario"] and request.POST["telefono_usuario"] and
    request.POST["piso_owner"] and request.POST["fecha_inicio"] and request.POST["fecha_fin"]
    and request.POST["huespedes"]:
        return True
    else:
        return False
"""