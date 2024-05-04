from drf_spectacular.utils import OpenApiParameter, OpenApiExample, inline_serializer
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .authentication import expires_in, token_expire_handler
from core.models import BaseUser, Demographics,PreOp,Phase1,Phase2
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
from .serializer import DemographicsSerializer,PreOpSerializer,PhaseOneSerializer,PhaseTwoSerializer

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
        user.license = data.get('license')
        user.save()
        data['username']=data['email']
        token_data=token_generator(data)
        del token_data['user']
        return {"success": True, "data":{"id":user.pk,'first_name': user.first_name, 'last_name': user.last_name, \
                                         'email':user.email,'role':user.role,'phone':user.phone,**token_data}}
    return {"success": False, "message": "User Already Exsist"}


def create_patient_user(data):
    user, is_created = BaseUser.objects.get_or_create(email=data.get("email"))
    if is_created:
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.phone = data.get("phone")
        user.password = make_password(data.get("password"))
        user.role = data.get('role')
        user.save()
        token_data=token_generator(data)
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
        if editable.get('doctor_email',None):
            updated=Demographics.objects.filter(id=request.data['id']).update(doctor=BaseUser.objects.get(email=editable['doctor_email']),doctors_history={editable['doctor_email']:DoctorApproval.OPEN})
            del editable['doctor_email']
        if editable.get('status',None):
            updated=Demographics.objects.filter(id=request.data['id']).update(status=DoctorApproval.INPROGRESS)
        if editable.get('percentage'):
            if editable.get('percentage') == 100:
                editable['current_phase'] == Phases.DEMOGRAPHICS
        updated=Demographics.objects.filter(id=request.data['id']).update(**editable)
        if updated:
            return "demographics data got updated"

def edit_preops(request):
    editable=request.data
    if editable.get('percentage'):
        demographics_obj=Demographics.objects.filter(id=editable.get('demographics_id'))
        if editable.get('percentage') == 100:
            demographics_obj.update(current_phase=Phases.PREOPS)
    updated=PreOp.objects.filter(demographics__id=editable.get('demographics_id')).update(**editable)
    if updated:
        return "Pre-Op data got updated"

def edit_phase1(request):
    editable=request.data
    if editable.get('percentage'):
        demographics_obj=Demographics.objects.filter(id=editable.get('demographics_id'))
        if editable.get('percentage') == 100:
            demographics_obj.update(current_phase=Phases.PHASE1)
    updated=Phase1.objects.filter(demographics__id=editable.get('demographics_id')).update(**editable)
    if updated:
        return "Phase1 data got updated"

def edit_phase2(request):
    editable=request.data
    if editable.get('percentage'):
        demographics_obj=Demographics.objects.filter(id=editable.get('demographics_id'))
        if editable.get('percentage') == 100:
            demographics_obj.update(current_phase=Phases.PHASE2)
    updated=Phase2.objects.filter(demographics__id=editable.get('demographics_id')).update(**editable)
    if updated:
        return "Phase2 data got updated"
    
def demographics_create(request):
    patient=BaseUser.objects.get(email=request.data['patient'])
    if request.data.get('doctor',None):
        doctors_history={request.data['doctor']:DoctorApproval.OPEN}
        doctor_obj=BaseUser.objects.get(email=request.data['doctor']) 
    else:
        doctors_history=doctor_obj=None
    if request.data.get('percentage') == 100:
        current_phase = Phases.DEMOGRAPHICS
    data={
            'country' : request.data.get('country',None),
            'gender' : request.data.get('gender',None),
            'dob' : request.data.get('dob',''),
            'height' : request.data.get('height',0),
            'weight' : request.data.get('weight',0),
            'sport' : request.data.get('sport',None),
            'current_activity' : request.data.get('current_activity',None),
            'date_of_injury' : request.data.get('date_of_injury',None),
            'knee' : request.data.get('knee',None),
            'mechanism_injury' : request.data.get('mechanism_injury',None),
            'other_injuries' : request.data.get('other_injuries',None),
            'injuries_same' : request.data.get('injuries_same',0),
            'injuries_other' : request.data.get('injuries_other',0),
            'reconstructions_same' : request.data.get('reconstructions_same',0),
            'reconstructions_other' : request.data.get('reconstructions_other',0),
            'planned_management' : request.data.get('planned_management',None),
            'survey_date' : request.data.get('survey_date',None),
            'doctor' :  doctor_obj,
            'doctors_history' : doctors_history,
            'patient': patient,
            'percentage' : request.data.get('percentage',0),
            'draft':request.data.get('draft',False),
            'current_phase' : current_phase
        }
    created = Demographics.objects.create(**data)
    if created:
        if doctor_obj and not request.data.get('draft',False):
            send_email_doctor(patient,doctor_obj.email)
            return "patient survey created and sent mail to doctor"
        return "patient survey created"

def create_preop(request):
    demographics_obj=Demographics.objects.filter(id=request.data.get('demographics_id'))
    if request.data.get('percentage') == 100:
        current_phase = Phases.PREOPS
        demographics_obj.update(current_phase=current_phase)
    data={
        "demographics":demographics_obj[0],
        "date":request.data.get('date',''),
        "passive_extension":request.data.get('passive_extension',0),
        "passive_flexion":request.data.get('passive_flexion',0),
        "swelling": request.data.get('swelling',None),
        "dynamometer_affected":request.data.get('dynamometer_affected',0),
        "dynamometer_non_affected":request.data.get('dynamometer_non_affected',0),
        "dynamometer_symmetry":request.data.get('dynamometer_symmetry',0),
        "hop_trial_1":request.data.get('hop_trial_1',0),
        "hop_trial_2":request.data.get('hop_trial_2',0),
        "hop_symmetry":request.data.get('hop_symmetry',0),
        "percentage":request.data.get('percentage',0),
        "draft":request.data.get('draft'),
    }
    created = PreOp.objects.create(**data)
    if created:
        return "Pre-Op data got created"

def create_phase1(request):
    demographics_obj=Demographics.objects.filter(id=request.data.get('demographics_id'))
    if request.data.get('percentage') == 100:
        current_phase = Phases.PHASE1
        demographics_obj.update(current_phase=current_phase)
    data={
        "demographics":demographics_obj[0],
        "date":request.data.get('date',''),
        "date_of_surgery":request.data.get('date_of_surgery',''),
        "percentage":request.data.get('percentage',0),
        "draft":request.data.get('draft'),
        "graft":request.data.get('graft',None),
        "passive_extension":request.data.get('passive_extension',0),
        "passive_flexion":request.data.get('passive_flexion',0),
        "swelling": request.data.get('swelling',None),
        "quads":request.data.get('quads',0),
    }
    created = Phase1.objects.create(**data)
    if created:
        return "Phase1 data got created"

def create_phase2(request):
    demographics_obj=Demographics.objects.filter(id=request.data.get('demographics_id'))
    if request.data.get('percentage') == 100:
        current_phase = Phases.PHASE2
        demographics_obj.update(current_phase=current_phase)
    data={
        "demographics":demographics_obj[0],
        "percentage":request.data.get('percentage',0),
        "draft":request.data.get('draft'),
        "date":request.data.get('date',''),
        "prone_hang":request.data.get('prone_hang',0),
        "passive_flexion":request.data.get('passive_flexion',0),
        "swelling": request.data.get('swelling',None),
        "functional_alignment": request.data.get('functional_alignment',None),
        "bridge_affected":request.data.get('bridge_affected',0),
        "bridge_non_affected":request.data.get('bridge_non_affected',0),
        "bridge_hurdle":request.data.get('bridge_hurdle',None),
        "bridge_symmetry":request.data.get('bridge_symmetry',0),
        "calf_affected":request.data.get('bridge_affected',0),
        "calf_non_affected":request.data.get('bridge_non_affected',0),
        "calf_hurdle":request.data.get('bridge_hurdle',None),
        "calf_symmetry":request.data.get('bridge_symmetry',0),
        "endurance_affected":request.data.get('bridge_affected',0),
        "endurance_non_affected":request.data.get('bridge_non_affected',0),
        "endurance_hurdle":request.data.get('bridge_hurdle',None),
        "endurance_symmetry":request.data.get('bridge_symmetry',0),
        "leg_rise_affected":request.data.get('bridge_affected',0),
        "leg_rise_non_affected":request.data.get('bridge_non_affected',0),
        "leg_rise_hurdle":request.data.get('bridge_hurdle',None),
        "leg_rise_symmetry":request.data.get('bridge_symmetry',0),
        "unipedal_open_affected":request.data.get('unipedal_open_affected',0),
        "unipedal_closed_affected":request.data.get('unipedal_closed_affected',0),
        "unipedal_open_non_affected":request.data.get('unipedal_open_non_affected',0),
        "unipedal_closed_non_affected":request.data.get('unipedal_closed_non_affected',0),
        "unipedal_affected_hurdel":request.data.get('unipedal_affected_hurdel',None),
        "unipedal_affected_non_hurdel":request.data.get('unipedal_non_affected_hurdel',None),
        "weight":request.data.get('weight',0),
        "leg_press_affected":request.data.get('leg_press_affected',0),
        "leg_press_affected_weight":request.data.get('leg_press_affected_weight',0),
        "leg_press_non_affected":request.data.get('leg_press_non_affected',0),
        "leg_press_non_affected_weight":request.data.get('leg_press_non_affected_weight',0),
        "squat":request.data.get('squat',0),
        "squat_weight":request.data.get('squat_weight',0),
    }
    created = Phase2.objects.create(**data)
    if created:
        return "Phase2 record got created"

def get_phases_doctor(data):
    current_phase = data[0].current_phase
    serializer_data = {}
    if current_phase == Phases.DEMOGRAPHICS:
            demographics_serializer = DemographicsSerializer(data,many=True)
            serializer_data['demographics']=demographics_serializer[0]
    if current_phase == Phases.PREOPS:
        demographics_serializer = DemographicsSerializer(data,many=True)
        data = PreOp.objects.filter(demographics_id=data[0].id)
        preop_serializer = PreOpSerializer(data,many=True)
        serializer_data['demographics']=demographics_serializer[0]
        serializer_data['preop']=preop_serializer[0]
    if current_phase == Phases.PHASE1:
        demographics_serializer = DemographicsSerializer(data,many=True)
        preop_data = PreOp.objects.filter(demographics_id=data[0].id)
        preop_serializer = PreOpSerializer(preop_data,many=True)
        phase1_data = Phase1.objects.filter(demographics_id=data[0].id)
        phase_one_serializer = PhaseOneSerializer(phase1_data,many=True)
        serializer_data['demographics']=demographics_serializer[0]
        serializer_data['preop']=preop_serializer[0]
        serializer_data['phase1']=phase_one_serializer[0]
    if current_phase == Phases.PHASE2:
        demographics_serializer = DemographicsSerializer(data,many=True)
        preop_data = PreOp.objects.filter(demographics_id=data[0].id)
        preop_serializer = PreOpSerializer(preop_data,many=True)
        phase1_data = Phase1.objects.filter(demographics_id=data[0].id)
        phase_one_serializer = PhaseOneSerializer(phase1_data,many=True)
        phase2_data = Phase2.objects.filter(demographics_id=data[0].id)
        phase_two_serializer = PhaseTwoSerializer(phase2_data,many=True)
        serializer_data['demographics']=demographics_serializer[0]
        serializer_data['preop']=preop_serializer[0]
        serializer_data['phase1']=phase_one_serializer[0]
        serializer_data['phase2']=phase_two_serializer[0]
    return serializer_data

def send_email_doctor(patient,doctor):
    login_link = "http://localhost:3000/login/"
    subject = 'New Survey request from patient'
    html_message = render_to_string('survey_doctor_email.html',{'patient':patient.first_name+' '+patient.last_name,'login_link': login_link})
    plain_message = strip_tags(html_message)
    to_email=[doctor,]  # Update with your sender email address
    send_mail(subject, plain_message,EMAIL_HOST_USER, to_email, html_message=html_message)