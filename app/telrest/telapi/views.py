from rest_framework.views import APIView
from rest_framework.response import Response
from security.jwt_gen import JWTEncoder
import time

class Index(APIView):

    def get(self, request, format=None):
        return Response(['Hello World'])


class Payload(APIView):

    def post(self, request, format=None):
        # 88 Nothing new
        # 101 Open Main Door
        # 235 Open Building Door
        nstrct = 235

        # Epoch
        seconds = time.time() + 3600

        # TODO iterator process
        payload = {
            'tmt': int(seconds),
            'nstrct': nstrct,
            'iterator': 0,
        }

        encoder = JWTEncoder()
        jwt = encoder.get_jwt(payload)
        response = {
            jwt.decode("utf-8")
        }

        return Response(response)
