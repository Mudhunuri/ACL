from drf_spectacular.utils import OpenApiParameter, OpenApiExample, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from django.db import transaction
from core.models import BaseUser
from django.contrib.auth.hashers import make_password
from core.constants import DOCTOR_ADMIN,PATIENT_ADMIN
from hashlib import sha1, sha256
import urllib.request, urllib.parse, urllib.error
from rest_framework.authtoken.models import Token
import base64


# def get_user_from_email():
#     adc_user = User.objects.filter(email=email)
#     if adc_user:
#         return adc_user[0]
#     return None

request_create_doctor = (
    inline_serializer(
        name='CustomSerializerCreatedoctor',
        fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
            'password': serializers.CharField(),
            'phone':  serializers.CharField(),
            'yoe': serializers.IntegerField(),
        }
    )
)

request_create_patient = (
    inline_serializer(
        name='CustomSerializerCreatepatient',
        fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
            'password': serializers.CharField(),
            'phone':  serializers.CharField(),
        }
    )
)

def generate_reset_password_link(user, host):
    """
    This function generate reset password link for the user.

    :param user: AdcUser object
    :returns: reset_password_url
    """
    token = Token.objects.get_or_create(user=user)
    salt = user.email[:5]  # Minimum length of an email address on Internet is 6 characters
    token = token[0]
    salted_token_key = token.key + salt
    hashed_salted_token_key = sha256(salted_token_key.encode()).hexdigest()
    adcuratio_url = host + 'reset_password'
    b64email = base64.b64encode(user.email.encode())
    reset_params = {"email": b64email,
                    "reset_token": hashed_salted_token_key}
    reset_password_url = '{0}?{1}'.format(adcuratio_url,
                                          urllib.parse.urlencode(reset_params))
    return reset_password_url


def reset_password_notification(user):
    from latrobe.settings import EMAIL_HOST_USER
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    reset_password_link = generate_reset_password_link(user=user,host="http://localhost:3000")
    subject = 'Reset Your Password'
    html_message = render_to_string('forgot_password_email.html', {'reset_password_link': reset_password_link})
    plain_message = strip_tags(html_message)
    to_email=['mudhunuri99@gmail.com',]  # Update with your sender email address
    print(user.email)
    #to_emails = ['mudhunuri99@gmail.com']
    #print(type(to_emails))

    send_mail(subject, plain_message,EMAIL_HOST_USER, to_email, html_message=html_message)

def get_user_from_email(email):
    """
    This function returns AdcUser object from email.

    :param email: email id
    :returns: AdcUser object or None
    """
    user = BaseUser.objects.filter(email=email)
    if user:
        return user[0]
    return None

def create_doctor_user(data):
    user, is_created = BaseUser.objects.get_or_create(email=data.get("email"))
    if is_created:
        user.first_name = data.get("firstname")
        user.last_name = data.get("lastname")
        user.phone = data.get("phone")
        user.experience = data.get("experience")
        user.degree =data.get('degree',None)
        user.password = make_password(data.get("password"))
        user.role = data.get('role')
        user.save()
        return {"success": True, "data":{"user_id":user.pk}}
    return {"success": False, "message": "User Already Exsist"}

def create_patient_user(data):
    user, is_created = BaseUser.objects.get_or_create(email=data.get("email"))
    if is_created:
        user.first_name = data.get("firstname")
        user.last_name = data.get("lastname")
        user.phone = data.get("phone")
        user.password = make_password(data.get("password"))
        user.role = data.get('role')
        user.save()
        return {"success": True, "data":{"user_id":user.pk}}
    return {"success": False, "message": "User Already Exsist"}

def reset_password(request):
    """
    Set a new password for the user if they are authorized

    :param request: {password}
    :return: {"success": True, "message": Return message}
    """
    password = request.data.get("password")
    email = request.data.get('email')
    if password:
        if len(password)> 26 and len(password) < 8 and (' ' in password):
            return {"success": False, "message":"Password must be more than 8 and less than 26 characters long and should not contain space."}
        if BaseUser.objects.filter(email=email).exists():
            user=BaseUser.objects.get(email=email)
        if make_password(password)!= user.password:
            user.set_password(password)
            user.save() 
            return {"success": True, "message": "new password successfully set."}
        else :
            return {"success": True, "message": "Please try a new password"}
    return {"success": False, "message": "all the fields are required"}