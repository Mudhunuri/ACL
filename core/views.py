from rest_framework.views import APIView
import json
from drf_spectacular.utils import extend_schema, inline_serializer
from django.http import HttpResponse
from rest_framework import renderers
from django.db.models import Q
from rest_framework.permissions import  AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import CharField, EmailField
from .constants import DOCTOR_ADMIN, PATIENT_ADMIN,Messages,DoctorApproval,Phases
from .serializer import Doctorserializer,DemographicsSerializer,PreOpSerializer,PhaseOneSerializer,PhaseTwoSerializer
from core.models import BaseUser,Demographics
from core.mixins import BaseApiMixin
from .helper import *

# Create your views here.
class ObtainAuthToken(APIView):
    """
    Auth token functionality.

    **Context**
    post:
    return a new token key with the user other information.

    """
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data=request.data
        data['username']=data['email']
        token_data=token_generator(data)
        val = {**token_data,'first_name': token_data['user'].first_name, 'last_name': token_data['user'].last_name}
        user=val['user']
        del val['user']
        if user.role == DOCTOR_ADMIN:
            data = {'id':user.id,'email':user.email,'role':user.role,'phone':user.phone,'experience':user.experience,'license':user.license,"related_data":'welcome to doctor portal'}
        elif user.role == PATIENT_ADMIN:
            data ={'id':user.id,'email':user.email,'role':user.role,'phone':user.phone,"related_data": 'welcome to patient portal'}
        else :
            data = HttpResponse(json.dumps(val),content_type='application/json')
            return data
        response = HttpResponse(json.dumps(dict(list(val.items())+list(data.items()))), content_type = 'application/json')
        return response


obtain_auth_token = ObtainAuthToken.as_view()

class EditUser(APIView):
    permission_classes = (AllowAny,)
    def put(self,request):
        user=BaseUser.objects.filter(email=request.data['email']).update(**request.data)
        if user:
            user=BaseUser.objects.get(email=request.data['email'])
            if user.role == PATIENT_ADMIN:
                data={'id':user.id,'email':user.email,'role':user.role,'phone':user.phone,'first_name':user.first_name,'last_name':user.last_name}
            elif user.role == DOCTOR_ADMIN:
                 data={'id':user.id,'email':user.email,'role':user.role,'phone':user.phone,'first_name':user.first_name,'last_name':user.last_name, 'experience':user.experience,'license':user.license}
            response = HttpResponse(json.dumps(dict(list(data.items()))), content_type = 'application/json')
            return response
        return Response({"success": False, "message": "User didn't got updated"})
        
class Register(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        try:
            #response = create_doctor_user(data=request.data)
            if request.data['role'] == 'doctor':
                response = create_doctor_user(data=request.data)
            elif request.data['role'] == 'patient':
                response = create_patient_user(data=request.data)
        except Exception as e:
            return Response({"success": False, "message": "Something went wrong","error":e})
        else:
            return Response(response)
        
class ForgotPassword(APIView):
    """
    View to send reset password for given email.
    **Context**

    post: Send reset password mail to the user mail id.
    """

    permission_classes = (AllowAny,)

    @extend_schema(request=inline_serializer(
            name='CustomForgotPasswordSerializer',
            fields={'email': EmailField(required=True)}
        )
    )
    def post(self, request):
        """
        Sends reset password email.
        ---
        parameters:
            - name: email
              required: true
        """
        email = request.data.get("email")
        if email is not None:
            user = get_user_from_email(email)
            if user is not None:
                reset_password_notification(user)
                response = {"success": True, "message": "Reset Password mail sent"}
            else:
                response = {"success": False, "message": "user does not exist with this email id."}
        else:
            response = {"success": False, "message": "email id is required."}
        return Response(response)

class ResetPassword(APIView):
    """
    View to reset password.
    **Context**

    post: Reset the password token send via mail.
    """
    #authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (AllowAny,)

    @extend_schema(request=inline_serializer(
            name='CustomResetPasswordSerializer',
            fields={'password': CharField(required=True)}
        )
    )
    def post(self, request):
        """
        Reset password of the user.
        ---
        parameters:
            - name: password
              required: true
        """
        response = reset_password(request)
        return Response(response)

class ListofDoctors(APIView,BaseApiMixin):
    permission_classes = (AllowAny,)
    def get(self, request):
        doctors_list=BaseUser.objects.filter(role=DOCTOR_ADMIN)
        if doctors_list.exists():
            seralizer=Doctorserializer(doctors_list,many=True)
            return self.success_response({Messages.SUCCESS: True, Messages.DATA: seralizer.data, Messages.MESSAGE: Messages.DATA_IS_VALID})
        return self.error_response({Messages.SUCCESS: False, Messages.DATA:[], Messages.MESSAGE: 'No Doctor data registered till now'})

class DemographicsView(APIView,BaseApiMixin):
    permission_classes = (AllowAny,)
    def post(self,request):
        if request.data['draft']:
            if not request.data.get('id',None):
                response=self.create_record(request)
            if request.data.get('id',None):
                response=self.edit_record(request)
        elif not request.data['draft']:
            if request.data.get('id',None):
                response=self.edit_record(request)
            else:
                response=self.create_record(request)
        return self.success_response({Messages.SUCCESS: True, Messages.DATA: response})
    
    def create_record(self,request): 
        response = ''
        if request.data.get('phase') == Phases.DEMOGRAPHICS:
            status,response=demographics_create(request)
        elif request.data.get('phase') == Phases.PREOPS:
            response=create_preop(request)
        elif request.data.get('phase') == Phases.PHASE1:
            response=create_phase1(request)
        elif request.data.get('phase') == Phases.PHASE2:
            response=create_phase2(request)
        elif request.data.get('phase') == Phases.PHASE3:
            response=create_phase3(request)
        elif request.data.get('phase') == Phases.PHASE4:
            response=create_phase4(request)
        return response
    
    def edit_record(self,request):
        response=''
        if not request.data.get('phase', None) or request.data.get('phase') == Phases.DEMOGRAPHICS:
            response=edit_demographics(request)
        elif request.data.get('phase') == Phases.PREOPS:
            response=edit_preops(request)
        elif request.data.get('phase') == Phases.PHASE1:
            response=edit_phase1(request)
        elif request.data.get('phase') == Phases.PHASE2:
            response=edit_phase2(request)
        elif request.data.get('phase') == Phases.PHASE3:
            response=edit_phase3(request)
        elif request.data.get('phase') == Phases.PHASE4:
            response=edit_phase4(request)
        return response

class DemographicsGetView(APIView,BaseApiMixin):
    permission_classes = (AllowAny,)
    def get(self,request):
        if request.GET.get('role') == PATIENT_ADMIN:
            data=Demographics.objects.filter(patient__email=request.GET.get('email'))
        elif request.GET.get('role') == DOCTOR_ADMIN:
            data=Demographics.objects.filter(Q(doctor__email=request.GET.get('email'))|Q(doctors_history__contains={request.GET.get('email'):DoctorApproval.CANCELLED})| \
                                             Q(doctors_history__contains={request.GET.get('email'):DoctorApproval.DECLINE}))
        serializer = DemographicsSerializer(data,many=True)
        return self.success_response({Messages.SUCCESS: True, Messages.DATA: serializer.data, Messages.MESSAGE: Messages.DATA_IS_VALID})

class GetCurrentPhase(APIView,BaseApiMixin):
    permission_classes = (AllowAny,)
    def get(self,request):
        data=[]
        if request.GET.get('role') == PATIENT_ADMIN:
            data=Demographics.objects.filter(patient__email=request.GET.get('email'))
        elif request.GET.get('role') == DOCTOR_ADMIN:
            data=Demographics.objects.filter(Q(doctor__email=request.GET.get('email'))|Q(doctors_history__contains={request.GET.get('email'):DoctorApproval.CANCELLED})| \
                                             Q(doctors_history__contains={request.GET.get('email'):DoctorApproval.DECLINE}))
        
        if data:
            serializer = DemographicsSerializer(data,many=True)
            return self.success_response({Messages.SUCCESS: True, Messages.DATA: serializer.data, Messages.MESSAGE: Messages.DATA_IS_VALID})
        return self.success_response({Messages.SUCCESS: True, Messages.DATA: data, Messages.MESSAGE:"No data present"})

class GetPhases(APIView,BaseApiMixin):
    permission_classes = (AllowAny,)
    def get(self,request):
        data=[]
        if request.GET.get('role') == PATIENT_ADMIN:
            obj=Demographics.objects.filter(id=request.GET.get('demographics_id'))
            result,progress=get_phases(obj)
            data.append(result)
        elif request.GET.get('role') == DOCTOR_ADMIN:
            obj=Demographics.objects.filter(id=request.GET.get('demographics_id'))
            data,progress = get_phases(obj)
        return self.success_response({Messages.SUCCESS: True, Messages.DATA: data+[{'progress':progress}], Messages.MESSAGE: Messages.DATA_IS_VALID})

class DemographicsEditView(APIView,BaseApiMixin):
    permission_classes = (AllowAny,)
    def put(self,request):
        updated=DemographicsView().edit_record(request)
        if updated:
            return self.success_response({Messages.SUCCESS: True,Messages.MESSAGE: 'updated successfully'})
        return self.error_response({Messages.SUCCESS: False,Messages.MESSAGE: 'couldnt update the data'})

class DemographicsDelete(APIView,BaseApiMixin):
    permission_classes = (AllowAny,)
    def delete(self,request):
        if Demographics.objects.filter(id=request.GET.get('id')).exists():
            Demographics.objects.filter(id=request.GET.get('id')).delete()
            return self.success_response({Messages.SUCCESS: True,Messages.MESSAGE: 'Survey deleted successfully'})
        return self.error_response({Messages.SUCCESS: False,Messages.MESSAGE: 'Requested record is not present in database'})
    
class DemographicsDoctorView(APIView,BaseApiMixin):
    permission_classes = (AllowAny,)
    def put(self,request):
        history={}
        obj=Demographics.objects.get(id=request.data['id'])
        email,history=obj.doctor.email,obj.doctors_history
        if request.data['accept'] == DoctorApproval.ACCEPT:
            history[email]=DoctorApproval.INPROGRESS
            Demographics.objects.filter(id=request.data['id']).update(doctors_history=history,status=DoctorApproval.INPROGRESS)
        else:
            history[email]=DoctorApproval.DECLINE
            Demographics.objects.filter(id=request.data['id']).update(doctors_history=history,status=DoctorApproval.DECLINE)
        return self.success_response({Messages.SUCCESS: True,Messages.MESSAGE: 'updated successfully'})


class DemographicsDoctorChange(APIView,BaseApiMixin):
    permission_classes = (AllowAny,)
    def put(self,request):
        doctor=request.data['doctor_email']
        obj=Demographics.objects.get(id=request.data['id'])
        email,history=obj.doctor.email,obj.doctors_history,obj.doctor
        history[email]=DoctorApproval.CANCELLED
        if email!=doctor:
            new_history={doctor:DoctorApproval.OPEN,**history}
            updated=Demographics.objects.filter(id=request.data['id']).update(doctors_history=new_history,doctor=BaseUser.objects.get(email=doctor))
            if updated:
                return self.success_response({Messages.SUCCESS: True,Messages.MESSAGE: 'updated successfully'})
        else:
            return self.error_response({Messages.SUCCESS: False,Messages.MESSAGE: 'Sending request to same doctor'})


