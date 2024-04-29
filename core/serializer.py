from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
#from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from core.models import BaseUser,Demographics


class Doctorserializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    first_name =serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    experience = serializers.ReadOnlyField()
    phone = serializers.ReadOnlyField()
    degree = serializers.ReadOnlyField()
    class Meta:
        model = BaseUser
        fields=('id','first_name','last_name','last_name','email','experience','phone','degree')

class DemographicsSerializer(serializers.ModelSerializer):
    country = serializers.ReadOnlyField()
    gender = serializers.ReadOnlyField()
    dob = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()
    weight = serializers.ReadOnlyField()
    sport =serializers.ReadOnlyField()
    current_activity = serializers.ReadOnlyField()
    date_of_injury = serializers.ReadOnlyField()
    knee = serializers.ReadOnlyField()
    mechanism_injury = serializers.ReadOnlyField()
    other_injuries = serializers.ReadOnlyField()
    injuries_same = serializers.ReadOnlyField()
    injuries_other = serializers.ReadOnlyField()
    reconstructions_same = serializers.ReadOnlyField()
    reconstructions_other = serializers.ReadOnlyField()
    planned_management = serializers.ReadOnlyField()
    survey_date =serializers.ReadOnlyField()
    patient_email =serializers.ReadOnlyField()
    patient_name = serializers.SerializerMethodField()
    doctor_email =serializers.ReadOnlyField(source='doctor.email')
    doctor_license = serializers.ReadOnlyField(source='doctor.license')
    doctors_history = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    #doctor_accepted = serializers.ReadOnlyField()
    percentage = serializers.ReadOnlyField()
    draft = serializers.ReadOnlyField()

    def get_patient_name(obj):
        return obj.patient.first_name+' '+obj.patient.last_name

    class Meta:
        model=Demographics
        fields = ('id','country','gender','dob',  'height','weight','sport','current_activity','date_of_injury' ,'knee' , \
                  'mechanism_injury','other_injuries' ,'injuries_same' ,'injuries_other' ,'reconstructions_same' ,'reconstructions_other','planned_management', \
                    'survey_date' ,'doctor_email','doctor_license' ,'doctors_history','status' ,'patient_email','patient_name','percentage','draft' )
        




