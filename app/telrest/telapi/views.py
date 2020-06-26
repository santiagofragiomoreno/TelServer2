from rest_framework.views import APIView
from rest_framework.response import Response
from security.jwt_gen import JWTEncoder

class Index(APIView):

    def get(self, request, format=None):
        return Response(['Hello World'])


class Payload(APIView):

    def post(self, request, format=None):
        # 88 Nothing new
        payload = {
            'time': 'test',
            'nstrct': 101,
            'iterator': 12,
        }

        # 101 Open Main Door
        payload = {
            'time': 'test',
            'nstrct': 101,
            'iterator': 12,
        }

        # 235 Open Building Door
        payload = {
            'time': 'test',
            'nstrct': 235,
            'iterator': 12,
        }

        encoder = JWTEncoder()
        jwt = encoder.get_jwt(payload)
        response = {
            jwt.decode("utf-8")
        }

        return Response(response)