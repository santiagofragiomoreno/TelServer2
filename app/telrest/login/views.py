import binascii
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from security.jwt_gen import JWTEncoder
import time
from telapi.models import Instruction, Task, Ownership, Grant, Access, SensorData, SensorType, FlatOwner, Flat
from security.permissions import IsIot, IsClient, IsSuperuser, IsOwner
import datetime
from .models import User_App, Reservation
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


def owner_log(request):
    context = {}
    template = loader.get_template('ownerlog.html')
    return HttpResponse(template.render(context, request))


# ---------use for login in BBDD-------------------


def consulting(request):
    context = {
        'ms': '',
        'user': False,
        'super': False,
        'staff': False
    }
    if request.POST["email"] and request.POST["password"]:
        username = request.POST["email"]
        password = request.POST["password"]
        # filter search in list if exists user with username and password equals at the form
        usuario = User.objects.filter(
        username__icontains=username, password__icontains=password)

        user = User.objects.get(username__icontains=username)

        request.session['user']=user.username
        request.session['userid']=user.id

        if usuario:
            if user.is_superuser:
                template = loader.get_template('admin/home.html')
                return HttpResponse(template.render(context, request))
        
            else:
                context['msg'] = request.session['user']
                template = loader.get_template('owner/navbar.html')
                return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('panel.ehlock.test/')
    else:
        return HttpResponseRedirect('panel.ehlock.test/')
