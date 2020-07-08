from rest_framework.views import APIView
from rest_framework.response import Response
from security.jwt_gen import JWTEncoder
import time
from telapi.models import Instruction, Task
from security.permissions import IsIot, IsClient, IsSuperuser, IsOwner
import datetime


class Index(APIView):

    def get(self, request, format=None):
        return Response(['OK'])


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


class CreateTask(APIView):
    permission_classes = [IsClient]

    def post(self, request, format=None):
        user = request.user

        return Response(['OK'])


class GiveGrant(APIView):
    permission_classes = [IsOwner]

    def post(self, request, format=None):
        user = request.user

        return Response(['OK'])
