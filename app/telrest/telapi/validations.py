import datetime

import pytz
from email_validator import validate_email, EmailNotValidError
from django.utils import timezone
from django.conf import settings


def validate_date(date_string):
    try:
        date_val = datetime.datetime.strptime(date_string, '%d-%m-%Y')
        date_val = date_val.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        return date_val
    except ValueError:
        return None


def validate_datetime(date_string):
    try:
        date_val = datetime.datetime.strptime(date_string, '%d-%m-%Y %H:%M')
        date_val = date_val.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
        return date_val
    except ValueError:
        return None


def validate_clientemail(client_email):
    try:
        # Validate.
        valid = validate_email(client_email,timeout=1)

        # Update with the normalized form.
        email = valid.email

        return email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        print(str(e))
        return None


def validate_integer(int_val):
    try:
        return int(int_val)
    except ValueError:
        return None
