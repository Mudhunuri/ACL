from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
#from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from core.models import BaseUser,Demographics,PreOp,Phase1,Phase2,Phase3,Phase4


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
    doctor =serializers.ReadOnlyField(source='doctor.email')
    doctor_name = serializers.SerializerMethodField()
    doctor_license = serializers.ReadOnlyField(source='doctor.license')
    doctors_history = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    #doctor_accepted = serializers.ReadOnlyField()
    percentage = serializers.ReadOnlyField()
    draft = serializers.ReadOnlyField()
    phase = serializers.ReadOnlyField(source='current_phase')

    def get_patient_name(self,obj):
        return obj.patient.first_name+' '+obj.patient.last_name
    
    def get_doctor_name(self,obj):
        if obj.doctor:
            return obj.doctor.first_name+' '+obj.doctor.last_name
        return None

    class Meta:
        model=Demographics
        fields = ('id','country','gender','dob',  'height','weight','sport','current_activity','date_of_injury' ,'knee' , \
                  'mechanism_injury','other_injuries' ,'injuries_same' ,'injuries_other' ,'reconstructions_same' ,'reconstructions_other','planned_management', \
                    'survey_date' ,'doctor','doctor_name','doctor_license' ,'doctors_history','status' ,'patient_email','patient_name','percentage','draft','phase' )
        
class PreOpSerializer(serializers.ModelSerializer):
    demographics_id=serializers.ReadOnlyField(source='demographics.id')
    date =serializers.ReadOnlyField()
    passive_extension =serializers.ReadOnlyField()
    passive_flexion =serializers.ReadOnlyField()
    swelling =serializers.ReadOnlyField()
    dynamometer_affected =serializers.ReadOnlyField()
    dynamometer_non_affected =serializers.ReadOnlyField()
    dynamometer_symmetry =serializers.ReadOnlyField()
    hop_trial_1_affected =serializers.ReadOnlyField()
    hop_trial_1_non_affected =serializers.ReadOnlyField()
    hop_trial_2_affected =serializers.ReadOnlyField()
    hop_trial_2_non_affected =serializers.ReadOnlyField()
    hop_symmetry =serializers.ReadOnlyField()
    percentage =serializers.ReadOnlyField()
    draft =serializers.ReadOnlyField()

    class Meta:
        model=PreOp
        fields = ('demographics_id','date','passive_extension','passive_flexion','swelling','dynamometer_affected', \
                  'dynamometer_non_affected','dynamometer_symmetry','hop_trial_1_affected','hop_trial_1_non_affected', \
                    'hop_trial_2_affected','hop_trial_2_non_affected','hop_symmetry','percentage','draft')

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
        model=Phase2
        fields = ('demographics_id','date','passive_flexion','swelling','percentage','draft','prone_hang','functional_alignment', \
                'bridge_affected','bridge_non_affected','bridge_hurdle','bridge_symmetry','calf_affected','calf_non_affected', \
                'calf_hurdle','calf_symmetry','endurance_affected','endurance_non_affected','endurance_hurdle','endurance_symmetry', \
                 'leg_rise_affected','leg_rise_non_affected','leg_rise_hurdle','leg_rise_symmetry','unipedal_open_affected', \
                  'unipedal_closed_affected','unipedal_open_non_affected','unipedal_closed_non_affected','unipedal_affected_hurdel', \
                   'unipedal_non_affected_hurdel','weight','leg_press_affected','leg_press_affected_weight','leg_press_non_affected', \
                   'leg_press_non_affected_weight','squat','squat_weight' )
        
class PhaseThreeSerializer(serializers.ModelSerializer):
    demographics_id=serializers.ReadOnlyField(source='demographics.id')
    percentage =serializers.ReadOnlyField()
    draft =serializers.ReadOnlyField()
    date =serializers.ReadOnlyField()
    hop_trial_1_affected =serializers.ReadOnlyField()
    hop_trial_1_non_affected =serializers.ReadOnlyField()
    hop_trial_2_affected =serializers.ReadOnlyField()
    hop_trial_2_non_affected =serializers.ReadOnlyField()
    hop_symmetry =serializers.ReadOnlyField()
    baseline_result =serializers.ReadOnlyField()
    affected_limb = serializers.ReadOnlyField()
    baseline_eq = serializers.ReadOnlyField()
    triple_trial_1_affected =serializers.ReadOnlyField()
    triple_trial_1_non_affected =serializers.ReadOnlyField()
    triple_trial_2_affected =serializers.ReadOnlyField()
    triple_trial_2_non_affected =serializers.ReadOnlyField()
    triple_symmetry =serializers.ReadOnlyField()
    crossover_trial_1_affected =serializers.ReadOnlyField()
    crossover_trial_1_non_affected =serializers.ReadOnlyField()
    crossover_trial_2_affected =serializers.ReadOnlyField()
    crossover_trial_2_non_affected =serializers.ReadOnlyField()
    crossover_symmetry =serializers.ReadOnlyField()
    side_trial_1_affected =serializers.ReadOnlyField()
    side_trial_1_non_affected =serializers.ReadOnlyField()
    side_symmetry =serializers.ReadOnlyField()
    triple_symmetry =serializers.ReadOnlyField()
    repetitions_affected =serializers.ReadOnlyField()
    repetitions_non_affected =serializers.ReadOnlyField()
    repetition_symmetry =serializers.ReadOnlyField()
    repetition_hurdle = serializers.ReadOnlyField()
    star_forward_affected = serializers.ReadOnlyField()
    star_forward_non_affected = serializers.ReadOnlyField()
    star_forward_symmetry = serializers.ReadOnlyField()
    postereomedical_affected  =serializers.ReadOnlyField()
    postereomedical_non_affected  =serializers.ReadOnlyField()
    postereolateral_affected  =serializers.ReadOnlyField()
    postereolateral_non_affected  =serializers.ReadOnlyField()
    postereo_symmetry  =serializers.ReadOnlyField()
    cooper_side_affected =  serializers.ReadOnlyField()
    cooper_side_non_affected =  serializers.ReadOnlyField()
    cooper_up_affected =  serializers.ReadOnlyField()
    cooper_up_non_affected =  serializers.ReadOnlyField()
    weight =serializers.ReadOnlyField()
    leg_affected =serializers.ReadOnlyField()
    leg_non_affected =serializers.ReadOnlyField()
    squat =serializers.ReadOnlyField()

    class Meta:
        model=Phase3
        fields=("demographics_id","percentage","draft","date","hop_trial_1_affected","hop_trial_1_non_affected","hop_trial_2_affected","hop_trial_2_non_affected", \
                "hop_symmetry","baseline_result","affected_limb","baseline_eq","triple_trial_1_affected","triple_trial_1_non_affected","triple_trial_2_affected","triple_trial_2_non_affected", \
                "triple_symmetry","crossover_trial_1_affected","crossover_trial_1_non_affected","crossover_trial_2_affected","crossover_trial_2_non_affected","crossover_symmetry","side_trial_1_affected", \
                "side_trial_1_non_affected","side_symmetry","triple_symmetry","repetitions_affected","repetitions_non_affected","repetition_symmetry","repetition_hurdle","star_forward_affected", \
                "star_forward_non_affected","star_forward_symmetry","postereomedical_affected","postereomedical_non_affected","postereolateral_affected","postereolateral_non_affected", "postereo_symmetry","cooper_side_affected","cooper_side_non_affected", \
                "cooper_up_affected","cooper_up_non_affected","weight","leg_affected","leg_non_affected","squat")
        
class PhaseFourSerializer(serializers.ModelSerializer):
    demographics_id=serializers.ReadOnlyField(source='demographics.id')
    percentage =serializers.ReadOnlyField()
    draft =serializers.ReadOnlyField()
    date =serializers.ReadOnlyField()
    dominant_leg = serializers.ReadOnlyField()
    swelling= serializers.ReadOnlyField()
    stability = serializers.ReadOnlyField()
    flexion = serializers.ReadOnlyField()
    extension = serializers.ReadOnlyField()
    aclrsi_q1 = serializers.ReadOnlyField() # first 3 question   
    aclrsi_q2 = serializers.ReadOnlyField()
    aclrsi_q3 = serializers.ReadOnlyField()
    ikdc_q1 = serializers.ReadOnlyField() # 2,3 ,6
    ikdc_q2 = serializers.ReadOnlyField()
    ikdc_q3 = serializers.ReadOnlyField()
    tsk_q1 = serializers.ReadOnlyField()# first 1,2,3
    tsk_q2 = serializers.ReadOnlyField()
    tsk_q3 = serializers.ReadOnlyField()
    result = serializers.ReadOnlyField()
    forward_affected  =serializers.ReadOnlyField()
    forward_non_affected  =serializers.ReadOnlyField()
    forward_symmetry =serializers.ReadOnlyField()
    postereomedical_affected  =serializers.ReadOnlyField()
    postereomedical_non_affected  =serializers.ReadOnlyField()
    postereolateral_affected  =serializers.ReadOnlyField()
    postereolateral_non_affected  =serializers.ReadOnlyField()
    postereo_symmetry =serializers.ReadOnlyField()
    cooper_side_affected =  serializers.ReadOnlyField()
    cooper_side_non_affected =  serializers.ReadOnlyField()
    cooper_up_affected =  serializers.ReadOnlyField()
    cooper_up_non_affected =  serializers.ReadOnlyField()
    hop_trial_1_affected =serializers.ReadOnlyField()
    hop_trial_1_non_affected =serializers.ReadOnlyField()
    hop_trial_2_affected =serializers.ReadOnlyField()
    hop_trial_2_non_affected =serializers.ReadOnlyField()
    hop_symmetry =serializers.ReadOnlyField()
    triple_trial_1_affected =serializers.ReadOnlyField()
    triple_trial_1_non_affected =serializers.ReadOnlyField()
    triple_trial_2_affected =serializers.ReadOnlyField()
    triple_trial_2_non_affected =serializers.ReadOnlyField()
    triple_symmetry =serializers.ReadOnlyField()
    crossover_trial_1_affected =serializers.ReadOnlyField()
    crossover_trial_1_non_affected =serializers.ReadOnlyField()
    crossover_trial_2_affected =serializers.ReadOnlyField()
    crossover_trial_2_non_affected =serializers.ReadOnlyField()
    crossover_symmetry =serializers.ReadOnlyField()
    side_trial_1_affected =serializers.ReadOnlyField()
    side_trial_1_non_affected =serializers.ReadOnlyField()
    side_symmetry =serializers.ReadOnlyField()
    repetitions_affected =serializers.ReadOnlyField()
    repetitions_non_affected =serializers.ReadOnlyField()
    repetition_symmetry =serializers.ReadOnlyField()
    test_1_name = serializers.ReadOnlyField()
    test_1_result = serializers.ReadOnlyField()
    test_1_baseline = serializers.ReadOnlyField()
    test_1_pass = serializers.ReadOnlyField()
    test_2_name= serializers.ReadOnlyField()
    test_2_result = serializers.ReadOnlyField()
    test_2_baseline = serializers.ReadOnlyField()
    test_2_pass = serializers.ReadOnlyField()
    fatigued_hop_trial_1_affected =serializers.ReadOnlyField()
    fatigued_hop_trial_1_non_affected =serializers.ReadOnlyField()
    fatigued_hop_trial_2_affected =serializers.ReadOnlyField()
    fatigued_hop_trial_2_non_affected =serializers.ReadOnlyField()
    fatigued_hop_symmetry =serializers.ReadOnlyField()
    fatigued_triple_trial_1_affected =serializers.ReadOnlyField()
    fatigued_triple_trial_1_non_affected =serializers.ReadOnlyField()
    fatigued_triple_trial_2_affected =serializers.ReadOnlyField()
    fatigued_triple_trial_2_non_affected =serializers.ReadOnlyField()
    fatigued_triple_symmetry =serializers.ReadOnlyField()
    fatigued_triple_trial_1_affected =serializers.ReadOnlyField()
    fatigued_triple_trial_1_non_affected =serializers.ReadOnlyField()
    fatigued_triple_trial_2_affected =serializers.ReadOnlyField()
    fatigued_triple_trial_2_non_affected =serializers.ReadOnlyField()
    fatigued_triple_symmetry =serializers.ReadOnlyField()
    fatigued_side_trial_1_affected =serializers.ReadOnlyField()
    fatigued_side_trial_1_non_affected =serializers.ReadOnlyField()
    fatigued_side_symmetry =serializers.ReadOnlyField()
    sport_score = serializers.ReadOnlyField()
    sport_hurdle =serializers.ReadOnlyField()

    class Meta:
        model=Phase4
        Fields=(
            "demographics","percentage","draft","date","dominant_leg","swelling","stability","flexion","extension","aclrsi_q1", \
            "aclrsi_q2","aclrsi_q3","ikdc_q1" ,"ikdc_q2","ikdc_q3","tsk_q1","tsk_q2" ,"tsk_q3" ,"result","forward_affected", \
            "forward_non_affected","forward_symmetry","postereomedical_affected","postereomedical_non_affected","postereolateral_affected", \
            "postereolateral_non_affected","postereo_symmetry","cooper_side_affected","cooper_side_non_affected","cooper_up_affected","cooper_up_non_affected", \
            "hop_trial_1_affected","hop_trial_1_non_affected","hop_trial_2_affected","hop_trial_2_non_affected","hop_symmetry","triple_trial_1_affected", \
            "triple_trial_1_non_affected","triple_trial_2_affected","triple_trial_2_non_affected","triple_symmetry","crossover_trial_1_affected", \
            "crossover_trial_1_non_affected","crossover_trial_2_affected","crossover_trial_2_non_affected","crossover_symmetry","side_trial_1_affected", \
            "side_trial_1_non_affected","side_symmetry","repetitions_affected","repetitions_non_affected","repetition_symmetry","test_1_name","test_1_result", \
            "test_1_baseline","test_1_pass","test_2_name","test_2_result","test_2_baseline","test_2_pass","fatigued_hop_trial_1_affected","fatigued_hop_trial_1_non_affected", \
            "fatigued_hop_trial_2_affected","fatigued_hop_trial_2_non_affected","fatigued_hop_symmetry","fatigued_triple_trial_1_affected","fatigued_triple_trial_1_non_affected", \
            "fatigued_triple_trial_2_affected","fatigued_triple_trial_2_non_affected","fatigued_triple_symmetry","fatigued_triple_trial_1_affected","fatigued_triple_trial_1_non_affected", \
            "fatigued_triple_trial_2_affected","fatigued_triple_trial_2_non_affected","fatigued_triple_symmetry","fatigued_side_trial_1_affected","fatigued_side_trial_1_non_affected", \
            "fatigued_side_symmetry","sport_score","sport_hurdle",
        )




