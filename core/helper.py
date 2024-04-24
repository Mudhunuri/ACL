from drf_spectacular.utils import OpenApiParameter, OpenApiExample, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from django.db import transaction
from core.model.base_models import Doctor
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from core.constants import DOCTOR_ADMIN,PATIENT_ADMIN

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

def create_doctor_user(data):
    user, is_created = Doctor.objects.get_or_create(email=data.get("email"))
    if is_created:
        user.first_name = data.get("firstname")
        user.last_name = data.get("lastname")
        user.phone = data.get("phone")
        user.experience = data.get("experience")
        user.degree =data.get('degree',None)
        user.password = make_password(data.get("password"))
        user.save()
        # group = Group.objects.get(name=DOCTOR_ADMIN)
        # group.user_set.add(user.pk)
        return {"success": True, "data":{"user_id":user.pk}}
    return {"success": False, "message": "User ALready Exsist"}

# def create_patient_user(data):
#     user, is_created = PatientUser.objects.get_or_create(email=data.get("email"))
#     if is_created:
#         user.first_name = data.get("firstname")
#         user.last_name = data.get("lastname")
#         user.phone = data.get("phone")
#         user.password = make_password(data.get("password"))
#         user.save()
#         group = Group.objects.get(name=PATIENT_ADMIN)
#         group.user_set.add(user.pk)
#         return {"success": True, "data":{"user_id":user.pk}}
#     return {"success": False, "message": "User ALready Exsist"}