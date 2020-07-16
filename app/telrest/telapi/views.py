import binascii
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from security.jwt_gen import JWTEncoder
import time
from telapi.models import Instruction, Task, Ownership, Grant, Access
from security.permissions import IsIot, IsClient, IsSuperuser, IsOwner
import datetime
from telapi.validations import validate_date, validate_datetime, validate_clientemail, validate_integer
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from django.template import loader
from django.http import HttpResponse, Http404

from security.authorization import InstructionAuthorization

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
    if not Instruction.objects.filter(
        task_id=1,
        recieved=0,
        user_id=2
    ).exists():
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
    if not Instruction.objects.filter(
        task_id=2,
        recieved=0,
        user_id=2
    ).exists():
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

        if Instruction.objects.exclude(recieved=1).filter(user=user).exists():
            next_instruction = Instruction.objects.exclude(recieved=1).filter(user=user).order_by('issued_date')[:1].get()
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
        access_code = access_code[0:12]

        grant = Grant(
            email=email,
            owner_user=user,
            iot_user_id=iot_id,
            access_code=access_code,
            start_date=start_date,
            end_date=end_date
        )

        try:
            grant.save()
        except:
            access_code = binascii.hexlify(os.urandom(20)).decode()
            access_code = access_code[0:12]
            grant.access_code = access_code
            grant.save()

        html_message = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><title>Open it yourself</title><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head><body style="margin: 0; padding: 0;"> <table border="0" cellpadding="0" cellspacing="0" width="100%"> <tr> <td style="padding: 10px 0 30px 0;"> <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border: 1px solid #cccccc; border-collapse: collapse;"> <tr> <td align="center" bgcolor="#fff" style="padding: 40px 0 30px 0; color: #153643; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif; padding:20px"> <img src="https://telfiregate.com/static/imgs/logo-large.png" alt="Open it yourself" width="100%" height="auto" style="display: block;"/> </td></tr><tr> <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;"> <table border="0" cellpadding="0" cellspacing="0" width="100%"> <tr> <td style="color: #153643; font-family: Arial, sans-serif; font-size: 24px;padding-bottom:8px"> <b>Here is your access code:</b> </td></tr><tr> <td style="color: #153643; font-family: Arial, sans-serif; font-size: 20px;"> <b>{{access_code}}</b> </td></tr><tr> <td style="padding: 20px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">Download the app and enter your code to be able to open the door of the house and much more!</td></tr><tr> <td> <table border="0" cellpadding="0" cellspacing="0" width="100%"> <tr> <td valign="top"><img src="https://blockduo.com/wp-content/uploads/2019/12/app-download-buttons-1.png" alt="Apps download" width="100%" height="auto" style="display: block;"/> </td></tr></table> </td></tr></table> </td></tr><tr> <td bgcolor="#ee4c50" style="padding: 30px 30px 30px 30px;"> <table border="0" cellpadding="0" cellspacing="0" width="100%"> <tr> <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" width="75%"> &reg; Openityourself S.L. 2020<br/> </td><td align="right" width="25%"> </td></tr></table> </td></tr></table> </td></tr></table></body></html>'

        html_message = html_message.replace('{{access_code}}',access_code)

        # send token to email and to owner
        send_mail('Your access code', 'Here is your code: '+access_code, 'noreply@openityourself.com', ['andressarnito@gmail.com'], fail_silently=False, html_message=html_message)

        return Response({'access_code': access_code})


class ActivateAccessCode(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        user = request.user

        post = request.POST

        # --- VALIDATIONS ---
        if 'access_code' not in post:
            raise APIException("Invalid request")

        # --- email ---
        if 'email' not in post:
            raise APIException("Invalid request")

        email = validate_clientemail(post['email'])
        if email is None:
            raise APIException("Invalid email")

        access_code = post['access_code'].replace(" ", "")  # remove spaces for injection prevention

        if not Grant.objects.filter(access_code=access_code, email=email, active=True).exists():
            raise APIException("Invalid access")

        grant = Grant.objects.get(access_code=access_code, email=email, active=True)

        # Generates Access Token
        access_token = binascii.hexlify(os.urandom(30)).decode()

        access_token_model = Access(
            grant=grant,
            token=access_token
        )
        access_token_model.save()

        # Expires grant
        grant.active = False
        grant.save()

        response = {
            'token': access_token_model.token,
            'start_date': grant.start_date,
            'end_date': grant.end_date,
        }

        return Response(response)


class InstructionView(APIView):
    authentication_classes = [InstructionAuthorization]
    permission_classes = []

    def post(self, request, format=None):
        grant = Grant.objects.get(id=request.user.grant_id)
        task = Task.objects.get(code=request.user.task_code)

        context = {}
        instruction = Instruction(
            task_id=task.id,
            recieved=0,
            user_id=grant.iot_user_id,
            grant_id=grant.id
        )
        if not Instruction.objects.filter(
            task_id=task.id,
            recieved=0,
            user_id=grant.iot_user_id,
            grant_id=grant.id
        ).exists():
            instruction.save()

        return Response(':)')