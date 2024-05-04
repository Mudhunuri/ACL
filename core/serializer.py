from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
#from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from core.models import BaseUser,Demographics,PreOp,Phase1,Phase2


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
    patient_email =serializers.ReadOnlyField(source='patient.email')
    patient_name = serializers.SerializerMethodField()
    doctor_email =serializers.ReadOnlyField(source='doctor.email')
    doctor_license = serializers.ReadOnlyField(source='doctor.license')
    doctors_history = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    #doctor_accepted = serializers.ReadOnlyField()
    percentage = serializers.ReadOnlyField()
    draft = serializers.ReadOnlyField()
    current_phase = serializers.ReadOnlyField()

    def get_patient_name(self,obj):
        return obj.patient.first_name+' '+obj.patient.last_name

    class Meta:
        model=Demographics
        fields = ('id','country','gender','dob',  'height','weight','sport','current_activity','date_of_injury' ,'knee' , \
                  'mechanism_injury','other_injuries' ,'injuries_same' ,'injuries_other' ,'reconstructions_same' ,'reconstructions_other','planned_management', \
                    'survey_date' ,'doctor_email','doctor_license' ,'doctors_history','status' ,'patient_email','patient_name','percentage','draft','current_phase' )
        
class PreOpSerializer(serializers.ModelSerializer):
    demographics_id=serializers.ReadOnlyField(source='demographics.id')
    date =serializers.ReadOnlyField()
    passive_extension =serializers.ReadOnlyField()
    passive_flexion =serializers.ReadOnlyField()
    swelling =serializers.ReadOnlyField()
    dynamometer_affected =serializers.ReadOnlyField()
    dynamometer_non_affected =serializers.ReadOnlyField()
    dynamometer_symmetry =serializers.ReadOnlyField()
    hop_trial_1 =serializers.ReadOnlyField()
    hop_trial_2 =serializers.ReadOnlyField()
    hop_symmetry =serializers.ReadOnlyField()
    percentage =serializers.ReadOnlyField()
    draft =serializers.ReadOnlyField()

    class Meta:
        model=PreOp
        fields = ('demographics_id','date','passive_extension','passive_flexion','swelling','dynamometer_affected', \
                  'dynamometer_non_affected','dynamometer_symmetry','hop_trial_1','hop_trial_2','hop_symmetry','percentage','draft')

class PhaseOneSerializer(serializers.ModelSerializer):
    demographics_id=serializers.ReadOnlyField(source='demographics.id')
    date =serializers.ReadOnlyField()
    date_of_surgery =serializers.ReadOnlyField()
    passive_extension =serializers.ReadOnlyField()
    passive_flexion =serializers.ReadOnlyField()
    swelling =serializers.ReadOnlyField()
    percentage =serializers.ReadOnlyField()
    draft =serializers.ReadOnlyField()
    graft =serializers.ReadOnlyField()
    quads =serializers.ReadOnlyField()

    class Meta:
        model=Phase1
        fields = ('demographics_id','date','graft','quads','date_of_surgery','passive_extension','passive_flexion','swelling','percentage','draft')

class PhaseTwoSerializer(serializers.ModelSerializer):
    demographics_id=serializers.ReadOnlyField(source='demographics.id')
    percentage =serializers.ReadOnlyField()
    draft =serializers.ReadOnlyField()
    date =serializers.ReadOnlyField()
    passive_flexion =serializers.ReadOnlyField()
    swelling =serializers.ReadOnlyField()
    prone_hang= serializers.ReadOnlyField()
    functional_alignment= serializers.ReadOnlyField()
    bridge_affected= serializers.ReadOnlyField()
    bridge_non_affected= serializers.ReadOnlyField()
    bridge_hurdle= serializers.ReadOnlyField()
    bridge_symmetry= serializers.ReadOnlyField()
    calf_affected= serializers.ReadOnlyField()
    calf_non_affected= serializers.ReadOnlyField()
    calf_hurdle= serializers.ReadOnlyField()
    calf_symmetry= serializers.ReadOnlyField()
    endurance_affected= serializers.ReadOnlyField()
    endurance_non_affected= serializers.ReadOnlyField()
    endurance_hurdle= serializers.ReadOnlyField()
    endurance_symmetry= serializers.ReadOnlyField()
    leg_rise_affected= serializers.ReadOnlyField()
    leg_rise_non_affected= serializers.ReadOnlyField()
    leg_rise_hurdle= serializers.ReadOnlyField()
    leg_rise_symmetry= serializers.ReadOnlyField()
    unipedal_open_affected= serializers.ReadOnlyField()
    unipedal_closed_affected= serializers.ReadOnlyField()
    unipedal_open_non_affected= serializers.ReadOnlyField()
    unipedal_closed_non_affected= serializers.ReadOnlyField()
    unipedal_affected_hurdel= serializers.ReadOnlyField()
    unipedal_non_affected_hurdel= serializers.ReadOnlyField()
    weight= serializers.ReadOnlyField()
    leg_press_affected= serializers.ReadOnlyField()
    leg_press_affected_weight= serializers.ReadOnlyField()
    leg_press_non_affected= serializers.ReadOnlyField()
    leg_press_non_affected_weight= serializers.ReadOnlyField()
    squat= serializers.ReadOnlyField()
    squat_weight= serializers.ReadOnlyField()

    class Meta:
        model=Phase1
        fields = ('demographics_id','date','passive_flexion','swelling','percentage','draft','prone_hang','functional_alignment', \
                'bridge_affected','bridge_non_affected','bridge_hurdle','bridge_symmetry','calf_affected','calf_non_affected', \
                'calf_hurdle','calf_symmetry','endurance_affected','endurance_non_affected','endurance_hurdle','endurance_symmetry', \
                 'leg_rise_affected','leg_rise_non_affected','leg_rise_hurdle','leg_rise_symmetry','unipedal_open_affected', \
                  'unipedal_closed_affected','unipedal_open_non_affected','unipedal_closed_non_affected','unipedal_affected_hurdel', \
                   'unipedal_non_affected_hurdel','weight','leg_press_affected','leg_press_affected_weight','leg_press_non_affected', \
                   'leg_press_non_affected_weight','squat','squat_weight' )

