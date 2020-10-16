import binascii
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from security.jwt_gen import JWTEncoder
import time
from telapi.models import Instruction, Task, Ownership, Grant, SensorData, SensorType, FlatOwner, Flat
from security.permissions import IsIot, IsClient, IsSuperuser, IsOwner
import datetime
#from .models import User_App, Reservation
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


def login_view(request):
    """ Custom login to redirect users to the superadmins or owners platform.
        django checks for the auth_user table from the database specified at the settings.DATABASES
        the values needed for the login saved during the session are username and password"""

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                request.session['user'] = user.username
                request.session['userid'] = user.id
                login(request, user)
                messages.success(request, 'Sesión iniciada')
                if user.is_superuser:
                    return redirect('/superadmin/')
                else:
                    return redirect('/owner/')
            else:
                messages.error(request, 'Usuario o contraseña inválidos')
        else:
            messages.error(request, 'Usuario o contraseña inválidos')

    form = AuthenticationForm()
    return render(request, 'ownerlog.html', context={'form': form})