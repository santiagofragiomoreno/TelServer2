from rest_framework.views import APIView
from rest_framework.response import Response
from security.permissions import IsOwner
from rest_framework.exceptions import APIException
from telapi.validations import validate_date, validate_datetime, validate_clientemail, validate_integer
import binascii
import os
from django.contrib.auth.models import User
from telapi.models import Instruction, Task, Ownership, Grant, Access, FlatOwner, Flat
from django.core.mail import send_mail
from django.forms.models import model_to_dict
from datetime import datetime
import pytz


class RequestClientAccess(APIView):
    permission_classes = [IsOwner]

    def post(self, request, format=None):
        user = request.user

        post = request.POST

        fields = [
            'start_date',
            'end_date',
            'flat_id',
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

        # --- Get iot_id ---
        # is int
        flat_id = validate_integer(form['flat_id'])
        if flat_id is None:
            raise APIException("Invalid id format")

        flat_owner = FlatOwner.objects.get(
            flat_id=flat_id,
            owner_user=user
        )
        iot_id = flat_owner.iot_user_id

        # --- iot id ---
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

        html_message = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><title>Open it yourself</title><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head><body style="margin: 0; padding: 0;"> <table border="0" cellpadding="0" cellspacing="0" width="100%"> <tr> <td style="padding: 10px 0 30px 0;"> <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border: 1px solid #cccccc; border-collapse: collapse;"> <tr> <td align="center" bgcolor="#fff" style="padding: 40px 0 30px 0; color: #153643; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif; padding:20px"> <img src="https://ehlock.com/assets/img/brand/logo-large.png" alt="Open it yourself" width="100%" height="auto" style="display: block;"/> </td></tr><tr> <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;"> <table border="0" cellpadding="0" cellspacing="0" width="100%"> <tr> <td style="color: #153643; font-family: Arial, sans-serif; font-size: 24px;padding-bottom:8px; text-align: center;"> <b>Here is your access code:</b> </td></tr><tr> <td style="color: #153643; font-family: Arial, sans-serif; font-size: 25px; text-align: center;padding-bottom:15px; padding-top:10px"> <b style="border: solid 1px #1b9aaa; padding: 4px">{{access_code}}</b> </td></tr><tr> <td style="padding: 20px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">Download the app and enter your code to be able to open the door of the house and much more!</td></tr><tr> <td> <table border="0" cellpadding="0" cellspacing="0" width="100%"> <tr> <td valign="top"><img src="https://blockduo.com/wp-content/uploads/2019/12/app-download-buttons-1.png" alt="Apps download" width="100%" height="auto" style="display: block;"/> </td></tr></table> </td></tr></table> </td></tr><tr> <td bgcolor="#1b9aaa" style="padding: 30px 30px 30px 30px;"> <table border="0" cellpadding="0" cellspacing="0" width="100%"> <tr> <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" width="75%"> &reg; Ehlock 2020<br/> </td><td align="right" width="25%"> </td></tr></table> </td></tr></table> </td></tr></table></body></html>'

        html_message = html_message.replace('{{access_code}}',access_code)

        # send token to email and to owner
        send_mail('Your access code', 'Here is your code: '+access_code, 'noreply@ehlock.com', [email], fail_silently=False, html_message=html_message)

        return Response({'access_code': access_code})


class MyFlats(APIView):
    permission_classes = [IsOwner]

    def post(self, request, format=None):
        user = request.user

        flats_owned = FlatOwner.objects.filter(
            owner_user=user
        ).values('flat_id')

        flats = Flat.objects.filter(
            id__in=flats_owned
        ).all()

        response = []

        for flat in flats:
            flat_fmt = model_to_dict(flat, fields=[field.name for field in flat._meta.fields])
            response.append(flat_fmt)

        return Response(response)


class Accesses(APIView):
    permission_classes = [IsOwner]

    def post(self, request, format=None):
        user = request.user
        post = request.POST

        grants_query = Grant.objects.filter(
            owner_user=user
        )

        if 'flat_id' in post:
            flat_id = int(post['flat_id'])

            iot_user_ids = FlatOwner.objects.filter(
                flat_id=flat_id
            ).values('iot_user_id')

            grants_query = grants_query.filter(
                iot_user_id__in=iot_user_ids
            )

        grants = grants_query.all()

        response = []
        utc = pytz.UTC
        present = datetime.now().replace(tzinfo=utc)

        for grant in grants:
            grant_fmt = model_to_dict(grant, fields=['id', 'email', 'start_date', 'end_date', 'active'])
            grant_fmt['created'] = grant.created

            start_time = grant.start_date.replace(tzinfo=utc)
            end_time = grant.end_date.replace(tzinfo=utc)

            if start_time <= present <= end_time:
                grant_fmt['vigor'] = True
            else:
                grant_fmt['vigor'] = False
            response.append(grant_fmt)

        return Response(response)

