import datetime

from rest_framework import authentication
from rest_framework import exceptions
from telapi.models import Access, Grant, InstructionUser
from django.contrib.auth.models import User
from django.conf import settings

import pytz

class InstructionAuthorization(authentication.BaseAuthentication):

    def authenticate(self, request):
        post = request.POST

        if 'token' not in post:
            raise exceptions.AuthenticationFailed("Forbidden 21")

        if 'sk' not in post:
            raise exceptions.AuthenticationFailed("Forbidden 31")

        token = post['token']

        if not Access.objects.filter(token=token, active=True).exists():
            raise exceptions.AuthenticationFailed("Not allowed 11")

        access = Access.objects.get(token=token, active=True)

        grant = access.grant

        now = self.set_time(datetime.datetime.now())

        if now < grant.start_date:
            raise exceptions.AuthenticationFailed("Not allowed 41")

        if now > grant.end_date:
            raise exceptions.AuthenticationFailed("Not allowed 51")

        try:
            task_code = int(post['sk'])
        except:
            raise exceptions.AuthenticationFailed("Not allowed 61")

        if task_code not in [101, 235]:
            raise exceptions.AuthenticationFailed("Not allowed 71")

        request_user = InstructionUser(
            grant_id=grant.id,
            access_id=access.id,
            task_code=task_code
        )

        return request_user, None

    @staticmethod
    def set_time(date_val):
        date_val = date_val.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        return date_val
