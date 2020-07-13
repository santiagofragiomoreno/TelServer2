import binascii
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from security.jwt_gen import JWTEncoder
import time
from telapi.models import Instruction, Task, Ownership, Grant
from security.permissions import IsIot, IsClient, IsSuperuser, IsOwner
import datetime
from telapi.validations import validate_date, validate_datetime, validate_clientemail, validate_integer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from django.template import loader
from django.http import HttpResponse, Http404


# ------------------------------------------------------------------------
def index(request):
    context = {}
    context['msg'] = ''
    template = loader.get_template('telapi/index.html')
    return HttpResponse(template.render(context, request))


def main_door(request):
    context = {}
    instruction = Instruction(
        task_id=1,
        recieved=0,
        user_id=2
    )
    instruction.save()
    context['msg'] = 'Main Door Opened'
    template = loader.get_template('telapi/index.html')
    return HttpResponse(template.render(context, request))


def building_door(request):
    context = {}
    instruction = Instruction(
        task_id=2,
        recieved=0,
        user_id=2
    )
    instruction.save()
    context['msg'] = 'Building Door Opened'
    template = loader.get_template('telapi/index.html')
    return HttpResponse(template.render(context, request))
# ------------------------------------------------------------------------

class Payload(APIView):
    permission_classes = [IsIot]

    def post(self, request, format=None):
        user = request.user

        # Epoch
        seconds = time.time() + 3600

        # 88 Nothing new
        # 101 Open Main Door
        # 235 Open Building Door
        nstrct = 88

        if Instruction.objects.filter(recieved__isnull=True, user=user).exists():
            next_instruction = Instruction.objects.filter(recieved__isnull=True, user=user).order_by('issued_date')[:1].get()
            nstrct = next_instruction.task.code
            next_instruction.recieved = 1
            next_instruction.recieved_date = datetime.datetime.now()
            next_instruction.save()

        payload = {
            'tmt': int(seconds),
            'nstrct': nstrct
        }

        encoder = JWTEncoder()
        jwt = encoder.get_jwt(payload)
        response = {
            jwt.decode("utf-8")
        }

        return Response(response)


class RequestClientAccess(APIView):
    permission_classes = [IsOwner]

    def post(self, request, format=None):
        user = request.user

        post = request.POST

        fields = [
            'start_date',
            'end_date',
            'iot_id',
            'client_email'
        ]

        form = {}

        for field in fields:
            if field not in post:
                raise APIException("Missing No")
            else:
                form[field] = post[field]

        # ------------------ Validations ------------------
        # --- Dates ---
        start_date = validate_datetime(form['start_date'])
        if start_date is None:
            raise APIException("Invalid date")

        end_date = validate_datetime(form['end_date'])
        if end_date is None:
            raise APIException("Invalid date")

        if start_date > end_date:
            raise APIException("Invalid date range")

        # --- email ---
        email = validate_clientemail(form['client_email'])
        if email is None:
            raise APIException("Invalid email")

        # --- iot id ---
        # is int
        iot_id = validate_integer(form['iot_id'])
        if iot_id is None:
            raise APIException("Invalid id format")
        # exists
        if not User.objects.filter(id=iot_id).exists():
            raise APIException("Invalid id")
        # is owned by user
        if not Ownership.objects.filter(owner_user_id=user.id, iot_user_id=iot_id, active=True).exists():
            raise APIException("Unauthorized")
        # ------------------------------------------------

        # Create Grant and generate Access Code
        access_code = binascii.hexlify(os.urandom(20)).decode()
        print(access_code)

        grant = Grant(
            email=email,
            owner_user=user,
            iot_user_id=iot_id,
            access_code=access_code,
            start_date=start_date,
            end_date=end_date
        )

        grant.save()

        # send token to email and to owner
        send_mail('Your access code', 'Here is your code: '+access_code, 'noreply@openityourself.com', ['andressarnito@gmail.com'], fail_silently=False)

        return Response({'access_code':access_code})


class ActivateAccessCode(APIView):
    permission_classes = [IsOwner]


    def post(self, request, format=None):
        user = request.user

        post = request.POST
        return Response(':)')


class TestOpenMain(APIView):
    authentication_classes = []

    def get(self, request, format=None):
        return Response(':)')