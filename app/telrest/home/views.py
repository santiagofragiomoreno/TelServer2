import binascii
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from security.jwt_gen import JWTEncoder
import time
from telapi.models import Instruction, Task, Ownership, Grant, Access, SensorData, SensorType
from security.permissions import IsIot, IsClient, IsSuperuser, IsOwner
import datetime
from telapi.validations import validate_date, validate_datetime, validate_clientemail, validate_integer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from django.template import loader
from django.http import HttpResponse, Http404

from security.authorization import InstructionAuthorization

def home(request):
    context = {}
    template = loader.get_template('home/home.html')
    return HttpResponse(template.render(context, request))
