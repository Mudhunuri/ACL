from drf_spectacular.utils import OpenApiParameter, OpenApiExample, inline_serializer
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .authentication import expires_in, token_expire_handler
from core.models import BaseUser, Demographics,PreOp,Phase1,Phase2,Phase3,Phase4
from django.contrib.auth.hashers import make_password
from core.constants import DOCTOR_ADMIN,PATIENT_ADMIN,DoctorApproval,Phases
from hashlib import sha1, sha256
import urllib.request, urllib.parse, urllib.error
from rest_framework.authtoken.models import Token
import base64
from rest_framework.authtoken.serializers import AuthTokenSerializer
from latrobe.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .serializer import DemographicsSerializer,PreOpSerializer,PhaseOneSerializer,PhaseTwoSerializer, \
PhaseThreeSerializer, PhaseFourSerializer
from datetime import datetime
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
    reset_password_link = generate_reset_password_link(user=user,host="http://localhost:3000/")
    subject = 'Reset Your Password'
    html_message = render_to_string('forgot_password_email.html', {'reset_password_link': reset_password_link})
    plain_message = strip_tags(html_message)
    to_email=[user.email,]  # Update with your sender email address
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

def token_generator(data):
    serializer=AuthTokenSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    is_expired, token = token_expire_handler(token)
    time_left = expires_in(token)
    return {'token': token.key, 'token_expires_in': str(time_left),'user':user}

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
        user.license = data.get('license','')
        user.save()
        data['username']=data['email']
        token_data=token_generator(data)
        del token_data['user']
        return {"success": True, "data":{"id":user.pk,'first_name': user.first_name, 'last_name': user.last_name, \
                                         'email':user.email,'role':user.role,'phone':user.phone,'experience':user.experience,'license':user.license,**token_data}}
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
        data['username']=data['email']
        token_data=token_generator(data)
        del token_data['user']
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


def edit_demographics(request):
    editable=request.data
    if Demographics.objects.get(id=request.data['id']).status == DoctorApproval.OPEN:
        if editable.get('doctor',None):
            updated=Demographics.objects.filter(id=request.data['id']).update(doctor=BaseUser.objects.get(email=editable['doctor']),doctors_history={editable['doctor_email']:DoctorApproval.OPEN})
            del editable['doctor']
        if editable.get('status',None):
            updated=Demographics.objects.filter(id=request.data['id']).update(status=DoctorApproval.INPROGRESS)
        if editable.get('percentage'):
            if editable.get('percentage') == 100:
                editable['current_phase'] = Phases.PREOPS
        if editable.get('phase',None):
            del editable['phase']
        updated=Demographics.objects.filter(id=request.data['id']).update(**editable)
        if updated:
            return "demographics data got updated"

def edit_preops(request):
    editable=request.data
    if editable.get('percentage'):
        demographics_obj=Demographics.objects.filter(id=editable.get('demographics_id'))
        if editable.get('percentage') == 100:
            demographics_obj.update(current_phase=Phases.PHASE1)
    del editable['phase']
    updated=PreOp.objects.filter(demographics__id=editable.get('demographics_id')).update(**editable)
    if updated:
        return "Pre-Op data got updated"

def edit_phase1(request):
    editable=request.data
    if editable.get('percentage'):
        demographics_obj=Demographics.objects.filter(id=editable.get('demographics_id'))
        if editable.get('percentage') == 100:
            demographics_obj.update(current_phase=Phases.PHASE2)
    del editable['phase']
    updated=Phase1.objects.filter(demographics__id=editable.get('demographics_id')).update(**editable)
    if updated:
        return "Phase1 data got updated"

def edit_phase2(request):
    editable=request.data
    if editable.get('percentage'):
        demographics_obj=Demographics.objects.filter(id=editable.get('demographics_id'))
        if editable.get('percentage') == 100:
            demographics_obj.update(current_phase=Phases.PHASE3)
    del editable['phase']
    updated=Phase2.objects.filter(demographics__id=editable.get('demographics_id')).update(**editable)
    if updated:
        return "Phase2 data got updated"

def edit_phase3(request):
    editable=request.data
    if editable.get('percentage'):
        demographics_obj=Demographics.objects.filter(id=editable.get('demographics_id'))
        if editable.get('percentage') == 100:
            demographics_obj.update(current_phase=Phases.PHASE4)
    del editable['phase']
    updated=Phase3.objects.filter(demographics__id=editable.get('demographics_id')).update(**editable)
    if updated:
        return "Phase3 data got updated"

def edit_phase4(request):
    editable=request.data
    if editable.get('percentage'):
        demographics_obj=Demographics.objects.filter(id=editable.get('demographics_id'))
        if editable.get('percentage') == 100:
            demographics_obj.update(current_phase=Phases.COMPLETED,status=Phases.COMPLETED)
    del editable['phase']
    updated=Phase4.objects.filter(demographics__id=editable.get('demographics_id')).update(**editable)
    if updated:
        return "Phase4 data got updated"
    
def demographics_create(request):
    patient=BaseUser.objects.get(email=request.data['patient_email'])
    if Demographics.objects.filter(patient__email=request.data['patient_email']).exists():
        return False,"Dear patient you already requsted for survey, if you wanted to procceed kindly complete/delete the existing survey"
    if request.data.get('doctor',None):
        doctors_history={request.data['doctor']:DoctorApproval.OPEN}
        doctor_obj=BaseUser.objects.get(email=request.data['doctor']) 
    else:
        doctors_history=doctor_obj=None 
    data={
            'country' : request.data.get('country',None),
            'gender' : request.data.get('gender',None),
            'dob' : request.data.get('dob')or None,
            'height' : request.data.get('height') or 0,
            'weight' : request.data.get('weight') or 0,
            'sport' : request.data.get('sport',None),
            'current_activity' : request.data.get('current_activity',None),
            'date_of_injury' : request.data.get('date_of_injury') or None,
            'knee' : request.data.get('knee',None),
            'mechanism_injury' : request.data.get('mechanism_injury',None),
            'other_injuries' : request.data.get('other_injuries',None),
            'injuries_same' : request.data.get('injuries_same') or 0,
            'injuries_other' : request.data.get('injuries_other') or 0,
            'reconstructions_same' : request.data.get('reconstructions_same') or 0,
            'reconstructions_other' : request.data.get('reconstructions_other') or 0,
            'planned_management' : request.data.get('planned_management',None),
            'survey_date' : request.data.get('survey_date'),
            'doctor' :  doctor_obj,
            'doctors_history' : doctors_history,
            'patient': patient,
            'percentage' : request.data.get('percentage'),
            'draft':request.data.get('draft',False),
            'current_phase' : Phases.PREOPS if request.data.get('percentage') == 100 else Phases.DEMOGRAPHICS
        }
    created = Demographics.objects.create(**data)
    if created:
        if doctor_obj and not request.data.get('draft',False):
            send_email_doctor(patient,doctor_obj.email)
            return True, "patient survey created and sent mail to doctor"
        return True,"patient survey created"

def create_preop(request):
    demographics_obj=Demographics.objects.filter(id=request.data.get('demographics_id'))
    if request.data.get('percentage') == 100:
        current_phase = Phases.PHASE1
        demographics_obj.update(current_phase=current_phase)
    data={
        "demographics":demographics_obj[0],
        "date":request.data.get('date') or None,
        "passive_extension":request.data.get('passive_extension') or 0,
        "passive_flexion":request.data.get('passive_flexion') or 0,
        "swelling": request.data.get('swelling',None),
        "dynamometer_affected":request.data.get('dynamometer_affected') or 0,
        "dynamometer_non_affected":request.data.get('dynamometer_non_affected') or 0,
        "dynamometer_symmetry":request.data.get('dynamometer_symmetry') or 0,
        "hop_trial_1_affected":request.data.get('hop_trial_1_affected') or 0,
        "hop_trial_1_non_affected":request.data.get('hop_trial_1_non_affected') or 0,
        "hop_trial_2_affected":request.data.get('hop_trial_2_affected') or 0,
        "hop_trial_2_non_affected":request.data.get('hop_trial_2_non_affected') or 0,
        "hop_symmetry":request.data.get('hop_symmetry') or 0,
        "percentage":request.data.get('percentage') or 0,
        "draft":request.data.get('draft'),
    }
    created = PreOp.objects.create(**data)
    if created:
        return "Pre-Op data got created"

def create_phase1(request):
    demographics_obj=Demographics.objects.filter(id=request.data.get('demographics_id'))
    if request.data.get('percentage') == 100:
        current_phase = Phases.PHASE2
        demographics_obj.update(current_phase=current_phase)
    data={
        "demographics":demographics_obj[0],
        "date":request.data.get('date') or None,
        "date_of_surgery":request.data.get('date_of_surgery') or None,
        "percentage":request.data.get('percentage'),
        "draft":request.data.get('draft'),
        "graft":request.data.get('graft',None),
        "passive_extension":request.data.get('passive_extension') or 0,
        "passive_flexion":request.data.get('passive_flexion') or 0,
        "swelling": request.data.get('swelling',None),
        "quads":request.data.get('quads') or 0,
    }
    created = Phase1.objects.create(**data)
    if created:
        return "Phase1 data got created"

def create_phase2(request):
    demographics_obj=Demographics.objects.filter(id=request.data.get('demographics_id'))
    if request.data.get('percentage') == 100:
        current_phase = Phases.PHASE3
        demographics_obj.update(current_phase=current_phase)
    data={
        "demographics":demographics_obj[0],
        "percentage":request.data.get('percentage') or 0,
        "draft":request.data.get('draft'),
        "date":request.data.get('date') or None,
        "prone_hang":request.data.get('prone_hang') or 0,
        "passive_flexion":request.data.get('passive_flexion') or 0,
        "swelling": request.data.get('swelling',None),
        "functional_alignment": request.data.get('functional_alignment',None),
        "bridge_affected":request.data.get('bridge_affected') or 0,
        "bridge_non_affected":request.data.get('bridge_non_affected') or 0,
        "bridge_hurdle":request.data.get('bridge_hurdle',None),
        "bridge_symmetry":request.data.get('bridge_symmetry') or 0,
        "calf_affected":request.data.get('bridge_affected') or 0,
        "calf_non_affected":request.data.get('bridge_non_affected') or 0,
        "calf_hurdle":request.data.get('bridge_hurdle',None),
        "calf_symmetry":request.data.get('bridge_symmetry') or 0,
        "endurance_affected":request.data.get('bridge_affected') or 0,
        "endurance_non_affected":request.data.get('bridge_non_affected') or 0,
        "endurance_hurdle":request.data.get('bridge_hurdle',None),
        "endurance_symmetry":request.data.get('bridge_symmetry') or 0,
        "leg_rise_affected":request.data.get('bridge_affected') or 0,
        "leg_rise_non_affected":request.data.get('bridge_non_affected') or 0,
        "leg_rise_hurdle":request.data.get('bridge_hurdle',None),
        "leg_rise_symmetry":request.data.get('bridge_symmetry') or 0,
        "unipedal_open_affected":request.data.get('unipedal_open_affected') or 0,
        "unipedal_closed_affected":request.data.get('unipedal_closed_affected') or 0,
        "unipedal_open_non_affected":request.data.get('unipedal_open_non_affected') or 0,
        "unipedal_closed_non_affected":request.data.get('unipedal_closed_non_affected') or 0,
        "unipedal_affected_hurdel":request.data.get('unipedal_affected_hurdel',None),
        "unipedal_affected_non_hurdel":request.data.get('unipedal_non_affected_hurdel',None),
        "weight":request.data.get('weight') or 0,
        "leg_press_affected":request.data.get('leg_press_affected') or 0,
        "leg_press_affected_weight":request.data.get('leg_press_affected_weight') or 0,
        "leg_press_non_affected":request.data.get('leg_press_non_affected') or 0,
        "leg_press_non_affected_weight":request.data.get('leg_press_non_affected_weight') or 0,
        "squat":request.data.get('squat') or 0,
        "squat_weight":request.data.get('squat_weight') or 0,
    }
    created = Phase2.objects.create(**data)
    if created:
        return "Phase2 record got created"
    
def create_phase3(request):
    demographics_obj=Demographics.objects.filter(id=request.data.get('demographics_id'))
    if request.data.get('percentage') == 100:
        current_phase = Phases.PHASE4
        demographics_obj.update(current_phase=current_phase)
    data={
        "demographics":demographics_obj[0],
        "percentage":request.data.get('percentage') or 0,
        "draft":request.data.get('draft'),
        "date":request.data.get('date') or None,
        "hop_trial_1_affected":request.data.get('hop_trial_1_affected') or 0,
        "hop_trial_1_non_affected":request.data.get('hop_trial_1_non_affected') or 0,
        "hop_trial_2_affected":request.data.get('hop_trial_2_affected') or 0,
        "hop_trial_2_non_affected":request.data.get('hop_trial_2_non_affected') or 0,
        "hop_symmetry":request.data.get('hop_symmetry') or 0,
        "baseline_result":request.data.get('baseline_result') or 0,
        "affected_limb":request.data.get('affected_limb') or 0,
        "baseline_eq":request.data.get('baseline_eq',None),
        "triple_trial_1_affected":request.data.get('triple_trial_1_affected') or 0,
        "triple_trial_1_non_affected": request.data.get('triple_trial_1_non_affected') or 0,
        "triple_trial_2_affected":request.data.get('triple_trial_2_affected') or 0,
        "triple_trial_2_non_affected": request.data.get('triple_trial_2_non_affected') or 0,
        "triple_symmetry":request.data.get('triple_symmetry') or 0,
        "crossover_trial_1_affected":request.data.get('crossover_trial_1_affected') or 0,
        "crossover_trial_1_non_affected":request.data.get('crossover_trial_1_non_affected') or 0,
        "crossover_trial_2_affected":request.data.get('crossover_trial_2_affected') or 0,
        "crossover_trial_2_non_affected":request.data.get('crossover_trial_2_non_affected') or 0,
        "crossover_symmetry":request.data.get('crossover_symmetry') or 0,
        "side_trial_1_affected":request.data.get('side_trial_1_affected') or 0,
        "side_trial_1_non_affected":request.data.get('side_trial_1_non_affected') or 0,
        "side_symmetry":request.data.get('side_symmetry') or 0,
        "triple_symmetry":request.data.get('triple_symmetry') or 0,
        "repetitions_affected":request.data.get('repetitions_affected') or 0,
        "repetitions_non_affected":request.data.get('repetitions_non_affected') or 0,
        "repetition_symmetry":request.data.get('repetition_symmetry') or 0,
        "repetition_hurdle":request.data.get('repetition_hurdle',None),
        "star_forward_affected":request.data.get('star_forward_affected') or 0,
        "star_forward_non_affected": request.data.get('star_forward_non_affected') or 0,
        "star_forward_symmetry":request.data.get('star_forward_symmetry') or 0,
        "postereomedical_affected": request.data.get('postereomedical_affected') or 0,
        "postereomedical_non_affected":request.data.get('postereomedical_non_affected') or 0,
        "postereolateral_affected": request.data.get('postereolateral_affected') or 0,
        "postereolateral_non_affected": request.data.get('postereolateral_non_affected') or 0,
        "postereo_symmetry":request.data.get('postereo_symmetry') or 0,
        "cooper_side_affected":request.data.get('cooper_side_affected',None),
        "cooper_side_non_affected": request.data.get('cooper_side_non_affected',None),
        "cooper_up_affected":request.data.get('cooper_up_affected',None),
        "cooper_up_non_affected":request.data.get('cooper_up_non_affected',None),
        "weight":request.data.get('weight') or 0,
        "leg_rm_affected":request.data.get('leg_rm_affected') or 0,
        "leg_weight_affected":request.data.get('leg_weight_affected') or 0,
        "leg_rm_non_affected":request.data.get('leg_rm_non_affected') or 0,
        "leg_weight_non_affected":request.data.get('leg_weight_non_affected') or 0,
        "squat_rm":request.data.get('squat_rm') or 0,
        "squat_weight":request.data.get('squat_weight') or 0,
    }
    created = Phase3.objects.create(**data)
    if created:
        return "Phase3 record got created"

def create_phase4(request):
    demographics_obj=Demographics.objects.filter(id=request.data.get('demographics_id'))
    if request.data.get('percentage') == 100:
        current_phase = Phases.COMPLETED
        demographics_obj.update(current_phase=current_phase,status=current_phase)
    data ={ 
    "demographics": demographics_obj[0],
    "percentage":request.data.get('percentage') or 0,
    "draft":request.data.get('draft'),
    "date":request.data.get('date',None),
    "dominant_leg":request.data.get('dominant_leg',None),
    "swelling":request.data.get('swelling',None),
    "stability":request.data.get('stability',None),
    "flexion":request.data.get('flexion',None),
    "extension":request.data.get('extension',None),
    "aclrsi_q1":request.data.get('aclrsi_q1') or 0,
    "aclrsi_q2":request.data.get('aclrsi_q2') or 0,
    "aclrsi_q3":request.data.get('aclrsi_q3') or 0,
    "ikdc_q1":request.data.get('ikdc_q1') or 0,
    "ikdc_q2":request.data.get('ikdc_q2') or 0,
    "ikdc_q3":request.data.get('ikdc_q3') or None,
    "tsk_q1":request.data.get('tsk_q1') or 0,
    "tsk_q2":request.data.get('tsk_q2') or 0, 
    "tsk_q3":request.data.get('tsk_q3') or 0,
    "result":request.data.get('result',None),
    "forward_affected":request.data.get('forward_affected') or 0,
    "forward_non_affected":request.data.get('forward_non_affected') or 0,
    "forward_symmetry":request.data.get('forward_symmetry') or 0,
    "postereomedical_affected":request.data.get('postereomedical_affected') or 0,
    "postereomedical_non_affected":request.data.get('postereomedical_non_affected') or 0,
    "postereolateral_affected":request.data.get('postereolateral_affected') or 0,
    "postereolateral_non_affected":request.data.get('postereolateral_non_affected') or 0,
    "postereo_symmetry":request.data.get('postereo_symmetry') or 0,
    "cooper_side_affected":request.data.get('cooper_side_affected',None),
    "cooper_side_non_affected":request.data.get('cooper_side_non_affected',None),
    "cooper_up_affected":request.data.get('cooper_up_affected',None),
    "cooper_up_non_affected":request.data.get('cooper_up_non_affected',None),
    "hop_trial_1_affected":request.data.get('hop_trial_1_affected') or 0,
    "hop_trial_1_non_affected":request.data.get('hop_trial_1_non_affected') or 0,
    "hop_trial_2_affected":request.data.get('hop_trial_2_affected') or 0,
    "hop_trial_2_non_affected":request.data.get('hop_trial_2_non_affected') or 0,
    "hop_symmetry":request.data.get('hop_symmetry') or 0,
    "triple_trial_1_affected":request.data.get('triple_trial_1_affected') or 0,
    "triple_trial_1_non_affected":request.data.get('triple_trial_1_non_affected') or 0,
    "triple_trial_2_affected":request.data.get('triple_trial_2_affected') or 0,
    "triple_trial_2_non_affected":request.data.get('triple_trial_2_non_affected') or 0,
    "triple_symmetry":request.data.get('triple_symmetry') or 0,
    "crossover_trial_1_affected":request.data.get('crossover_trial_1_affected') or 0,
    "crossover_trial_1_non_affected":request.data.get('crossover_trial_1_non_affected') or 0,
    "crossover_trial_2_affected":request.data.get('crossover_trial_2_affected') or 0,
    "crossover_trial_2_non_affected":request.data.get('crossover_trial_2_non_affected') or 0,
    "crossover_symmetry":request.data.get('crossover_symmetry') or 0,
    "side_trial_1_affected":request.data.get('side_trial_1_affected') or 0,
    "side_trial_1_non_affected":request.data.get('side_trial_1_non_affected') or 0,
    "side_symmetry":request.data.get('side_symmetry') or 0,
    "repetitions_affected":request.data.get('repetitions_affected') or 0,
    "repetitions_non_affected":request.data.get('repetitions_non_affected') or 0,
    "repetition_symmetry":request.data.get('repetition_symmetry') or 0,
    "test_1_name":request.data.get('test_1_name',None),
    "test_1_result":request.data.get('test_1_result',None),
    "test_1_baseline":request.data.get('test_1_baseline',None),
    "test_1_pass":request.data.get('test_1_pass',None),
    "test_2_name":request.data.get('test_2_name',None),
    "test_2_result":request.data.get('test_2_result',None),
    "test_2_baseline":request.data.get('test_2_baseline',None),
    "test_2_pass":request.data.get('test_2_pass',None),
    "fatigued_hop_trial_1_affected":request.data.get('fatigued_hop_trial_1_affected') or 0,
    "fatigued_hop_trial_1_non_affected":request.data.get('fatigued_hop_trial_1_non_affected') or 0,
    "fatigued_hop_trial_2_affected":request.data.get('fatigued_hop_trial_2_affected') or 0,
    "fatigued_hop_trial_2_non_affected":request.data.get('fatigued_hop_trial_2_non_affected') or 0,
    "fatigued_hop_symmetry":request.data.get('fatigued_hop_symmetry') or 0,
    "fatigued_triple_trial_1_affected":request.data.get('fatigued_triple_trial_1_affected') or 0,
    "fatigued_triple_trial_1_non_affected":request.data.get('fatigued_triple_trial_1_non_affected') or 0,
    "fatigued_triple_trial_2_affected":request.data.get('fatigued_triple_trial_2_affected') or 0,
    "fatigued_triple_trial_2_non_affected":request.data.get('fatigued_triple_trial_2_non_affected') or 0,
    "fatigued_triple_symmetry":request.data.get('fatigued_triple_symmetry') or 0,
    "fatigued_triple_trial_1_affected":request.data.get('fatigued_triple_trial_1_affected') or 0,
    "fatigued_triple_trial_1_non_affected":request.data.get('fatigued_triple_trial_1_non_affected') or 0,
    "fatigued_triple_trial_2_affected":request.data.get('fatigued_triple_trial_2_affected') or 0,
    "fatigued_triple_trial_2_non_affected":request.data.get('fatigued_triple_trial_2_non_affected') or 0,
    "fatigued_triple_symmetry":request.data.get('fatigued_triple_symmetry') or 0,
    "fatigued_side_trial_1_affected":request.data.get('fatigued_side_trial_1_affected') or 0,
    "fatigued_side_trial_1_non_affected":request.data.get('fatigued_side_trial_1_non_affected') or 0,
    "fatigued_side_symmetry":request.data.get('fatigued_side_symmetry') or 0,
    "sport_score":request.data.get('sport_score') or 0,
    "sport_hurdle":request.data.get('sport_hurdle') or 0
    }
    created = Phase4.objects.create(**data)
    if created:
        return "Phase4 record got created"

def get_phases(data):
    current_phase = data[0].current_phase
    list_phases=[]
    serializer_data = {}
    progress_list = [0]*6
    progress_list[0]=data.first().percentage
    if current_phase == Phases.DEMOGRAPHICS:
            demographics_serializer = DemographicsSerializer(data,many=True)
            serializer_data[Phases.DEMOGRAPHICS]=demographics_serializer.data[0]
    if current_phase == Phases.PREOPS:
        demographics_serializer = DemographicsSerializer(data,many=True)
        serializer_data[Phases.DEMOGRAPHICS]=demographics_serializer.data[0]
        if PreOp.objects.filter(demographics__id=data[0].id).exists():
            data = PreOp.objects.filter(demographics__id=data[0].id)
            preop_serializer = PreOpSerializer(data,many=True)
            serializer_data[Phases.PREOPS]=preop_serializer.data[0]
            progress_list[1]=data.first().percentage
    if current_phase == Phases.PHASE1:
        demographics_serializer = DemographicsSerializer(data,many=True)
        preop_data = PreOp.objects.filter(demographics__id=data[0].id)
        preop_serializer = PreOpSerializer(preop_data,many=True)
        serializer_data[Phases.DEMOGRAPHICS]=demographics_serializer.data[0]
        serializer_data[Phases.PREOPS]=preop_serializer.data[0]
        progress_list[1]=preop_data.first().percentage
        if Phase1.objects.filter(demographics__id=data[0].id).exists():
            phase1_data = Phase1.objects.filter(demographics__id=data[0].id)
            phase_one_serializer = PhaseOneSerializer(phase1_data,many=True)
            serializer_data[Phases.PHASE1]=phase_one_serializer.data[0]
            progress_list[2]=phase1_data.first().percentage
    if current_phase == Phases.PHASE2:
        demographics_serializer = DemographicsSerializer(data,many=True)
        preop_data = PreOp.objects.filter(demographics__id=data[0].id)
        preop_serializer = PreOpSerializer(preop_data,many=True)
        phase1_data = Phase1.objects.filter(demographics__id=data[0].id)
        phase_one_serializer = PhaseOneSerializer(phase1_data,many=True)
        serializer_data[Phases.DEMOGRAPHICS]=demographics_serializer.data[0]
        serializer_data[Phases.PREOPS]=preop_serializer.data[0]
        serializer_data[Phases.PHASE1]=phase_one_serializer.data[0]
        progress_list[1]=preop_data.first().percentage
        progress_list[2]=phase1_data.first().percentage
        if Phase2.objects.filter(demographics__id=data[0].id).exists():
            phase2_data = Phase2.objects.filter(demographics__id=data[0].id)
            phase_two_serializer = PhaseTwoSerializer(phase2_data,many=True)
            serializer_data[Phases.PHASE2]=phase_two_serializer.data[0]
            progress_list[3]=phase2_data.first().percentage
    if current_phase == Phases.PHASE3:
        demographics_serializer = DemographicsSerializer(data,many=True)
        preop_data = PreOp.objects.filter(demographics__id=data[0].id)
        preop_serializer = PreOpSerializer(preop_data,many=True)
        phase1_data = Phase1.objects.filter(demographics__id=data[0].id)
        phase_one_serializer = PhaseOneSerializer(phase1_data,many=True)
        phase2_data = Phase2.objects.filter(demographics__id=data[0].id)
        phase_two_serializer = PhaseTwoSerializer(phase2_data,many=True)
        serializer_data[Phases.DEMOGRAPHICS]=demographics_serializer.data[0]
        serializer_data[Phases.PREOPS]=preop_serializer.data[0]
        serializer_data[Phases.PHASE1]=phase_one_serializer.data[0]
        serializer_data[Phases.PHASE2]=phase_two_serializer.data[0]
        progress_list[1]=preop_data.first().percentage
        progress_list[2]=phase1_data.first().percentage
        progress_list[3]=phase2_data.first().percentage
        if Phase3.objects.filter(demographics__id=data[0].id).exists():
            phase3_data = Phase3.objects.filter(demographics__id=data[0].id)
            phase_three_serializer = PhaseThreeSerializer(phase3_data,many=True)
            serializer_data[Phases.PHASE3]=phase_three_serializer.data[0]
            progress_list[4]=phase3_data.first().percentage
    if current_phase == Phases.PHASE4:
        demographics_serializer = DemographicsSerializer(data,many=True)
        preop_data = PreOp.objects.filter(demographics__id=data[0].id)
        preop_serializer = PreOpSerializer(preop_data,many=True)
        phase1_data = Phase1.objects.filter(demographics__id=data[0].id)
        phase_one_serializer = PhaseOneSerializer(phase1_data,many=True)
        phase2_data = Phase2.objects.filter(demographics__id=data[0].id)
        phase_two_serializer = PhaseTwoSerializer(phase2_data,many=True)
        serializer_data[Phases.DEMOGRAPHICS]=demographics_serializer.data[0]
        serializer_data[Phases.PREOPS]=preop_serializer.data[0]
        serializer_data[Phases.PHASE1]=phase_one_serializer.data[0]
        serializer_data[Phases.PHASE2]=phase_two_serializer.data[0]
        phase3_data = Phase3.objects.filter(demographics__id=data[0].id)
        phase_three_serializer = PhaseThreeSerializer(phase3_data,many=True)
        serializer_data[Phases.PHASE3]=phase_three_serializer.data[0]
        progress_list[1]=preop_data.first().percentage
        progress_list[2]=phase1_data.first().percentage
        progress_list[3]=phase2_data.first().percentage
        progress_list[4]=phase3_data.first().percentage
        if Phase4.objects.filter(demographics__id=data[0].id).exists():
            phase4_data = Phase4.objects.filter(demographics__id=data[0].id)
            phase_four_serializer = PhaseFourSerializer(phase4_data,many=True)
            serializer_data[Phases.PHASE4]=phase_four_serializer.data[0]
            progress_list[5]=phase4_data.first().percentage
        
    list_phases.append(serializer_data)
    return list_phases

def send_email_doctor(patient,doctor):
    login_link = "http://localhost:3000/login/"
    subject = 'New Survey request from patient'
    html_message = render_to_string('survey_doctor_email.html',{'patient':patient.first_name+' '+patient.last_name,'login_link': login_link})
    plain_message = strip_tags(html_message)
    to_email=[doctor,]  # Update with your sender email address
    send_mail(subject, plain_message,EMAIL_HOST_USER, to_email, html_message=html_message)