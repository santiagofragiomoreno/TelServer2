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

# ------------------------------------------------------------------------
#Request contiene enlaces GET de urls de origen o destino
def index(request):
    context = {}
    context['msg'] = ''
    template = loader.get_template('telapi/index.html')
    return HttpResponse(template.render(context, request))


def log_molino(request):
    context = {}
    user_id = 5

    # Last instructions:
    last_instructions_flat = Instruction.objects.filter(
        user_id=user_id,
        task_id=1
    ).order_by('-issued_date').all()[:20]

    last_instructions_building = Instruction.objects.filter(
        user_id=user_id,
        task_id=2
    ).order_by('-issued_date').all()[:20]

    tasks = Task.objects.all()

    sensor_data_door = SensorData.objects.filter(
        iot_user=user_id,
        sensor_type_id=1
    ).order_by('-created').all()[:50]

    sensor_data_mov = SensorData.objects.filter(
        iot_user=user_id,
        sensor_type_id=2
    ).order_by('-created').all()[:50]

    sensor_types = SensorType.objects.all()

    # --- instructions ---
    instructions_building_door = []
    instructions_flat_door = []
    for instruction in last_instructions_flat:
        instruction_fmt = {
            'issued_date':instruction.issued_date,
            'recieved_date':instruction.issued_date,
            'recieved':instruction.recieved
        }
        instructions_flat_door.append(instruction_fmt)
    context['instructions_flat_door'] = instructions_flat_door

    for instruction in last_instructions_building:
        instruction_fmt = {
            'issued_date':instruction.issued_date,
            'recieved_date':instruction.issued_date,
            'recieved':instruction.recieved
        }
        instructions_building_door.append(instruction_fmt)
    context['instructions_building_door'] = instructions_building_door


    # --- sensors ---
    lock_data = []
    movement_data = []
    for data in sensor_data_door:
        #  - Lock
        created_val = data.created
        lock_data.append(created_val)

    for data in sensor_data_mov:
        #  - Movement
        created_val = data.created
        movement_data.append(created_val)

    context['lock_data'] = lock_data
    context['movement_data'] = movement_data

    template = loader.get_template('telapi/molino.html')
    return HttpResponse(template.render(context, request))

#Genera la peticion para la apertura de portal y coloca en un "JSON" la informacion para la BBDD (Molina)
#Realmente es una inserccion que se almacena en la tabla instruction las fechas se hacen de forma automatica

def main_door_iot2(request):
    context = {}
    context['msg'] = ''
    if request.method == 'POST':
        instruction = Instruction(
            task_id=1,
            recieved=0,
            user_id=5,
            grant_id=2
        )
        if not Instruction.objects.filter(
            task_id=1,
            recieved=0,
            user_id=5,
            grant_id=2
        ).exists():
            instruction.save()
        context['msg'] = 'Main Door Opened'
    template = loader.get_template('telapi/index.html')
    return HttpResponse(template.render(context, request))


def building_door_iot2(request):
    context = {}
    context['msg'] = ''
    if request.method == 'POST':
        instruction = Instruction(
            task_id=2,
            recieved=0,
            user_id=5,
            grant_id=2
        )
        if not Instruction.objects.filter(
            task_id=2,
            recieved=0,
            user_id=5,
            grant_id=2
        ).exists():
            instruction.save()
        context['msg'] = 'Building Door Opened'
    template = loader.get_template('telapi/index.html')
    return HttpResponse(template.render(context, request))

# iot_3 = Cerradura oficina
def main_door_iot3(request):
    context = {}
    context['msg'] = ''
    if request.method == 'POST':
        instruction = Instruction(
            task_id=1,
            recieved=0,
            user_id=6,
            grant_id=3
        )
        if not Instruction.objects.filter(
            task_id=1,
            recieved=0,
            user_id=6,
            grant_id=3
        ).exists():
            instruction.save()
        context['msg'] = 'Main Door Opened'
    template = loader.get_template('telapi/index.html')
    return HttpResponse(template.render(context, request))


def building_door_iot3(request):
    context = {}
    context['msg'] = ''
    if request.method == 'POST':
        instruction = Instruction(
            task_id=2,
            recieved=0,
            user_id=6,
            grant_id=3
        )
        if not Instruction.objects.filter(
            task_id=2,
            recieved=0,
            user_id=6,
            grant_id=3
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
        post = request.POST

        # --- POST PAYLOAD ---
        if 'lockstatus' in post:
            lockstatus = int(post['lockstatus'])

            if lockstatus != 0:
                sensor_data_lock = SensorData(
                    iot_user=user,
                    sensor_type_id=1,
                    value=lockstatus
                )
                sensor_data_lock.save()

        if 'movementstatus' in post:
            movementstatus = int(post['movementstatus'])

            if movementstatus != 0:
                sensor_data_mov = SensorData(
                    iot_user=user,
                    sensor_type_id=2,
                    value=movementstatus
                )
                sensor_data_mov.save()

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

#Apiview rellena request con items e informacion de la propia pagina
class ActivateAccessCode(APIView):
    authentication_classes = []
    permission_classes = []
#Metodo envia en POST la peticion de abrir puerta
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
        #Coge los access_code y elimina todo los huecos en blanco
        access_code = post['access_code'].replace(" ", "")  # remove spaces for injection prevention

        if not Grant.objects.filter(access_code=access_code, email=email, active=True).exists():
            raise APIException("Invalid access")

        grant = Grant.objects.get(access_code=access_code, email=email, active=True)

        # Generates Access Token
        access_token = binascii.hexlify(os.urandom(30)).decode()
        #genera el json con el access_token
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
            user_id=grant.iot_user_id
        ).exists():
            instruction.save()
            return Response({'result': 'ok'})

        return Response({'result': 'exists'})
