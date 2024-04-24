from rest_framework.views import APIView
import json
from drf_spectacular.utils import extend_schema, inline_serializer
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import renderers, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import CharField, EmailField, ChoiceField
from .authentication import expires_in, token_expire_handler
from .constants import DOCTOR_ADMIN, PATIENT_ADMIN
from .serializer import CustomAuthTokenSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from .model.base_models import Doctor
from .helper import request_create_doctor,request_create_patient,create_doctor_user

# Create your views here.
class ObtainAuthToken(APIView):
    """
    Auth token functionality.

    **Context**
    post:
    return a new token key with the user other information.

    """
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = CustomAuthTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        is_expired, token = token_expire_handler(token)
        time_left = expires_in(token)

        val = {'token': token.key, 'token_expires_in': str(time_left), 'role': request.data['role'],'first_name': user.first_name, 'last_name': user.last_name}

        if request.data['role'] == DOCTOR_ADMIN:
            data = {"related_data":'welcome to doctor portal'}

        elif request.data['role'] == PATIENT_ADMIN:
            data ={"related_data": 'welcome to patient portal'}

        else :
            data = HttpResponse(json.dumps(val),content_type='application/json')
            return data
        response = HttpResponse(json.dumps(dict(list(val.items())+list(data.items()))), content_type = 'application/json')
        return response


obtain_auth_token = ObtainAuthToken.as_view()


class Login(APIView):
    def post(self, request):
        import pdb;pdb.set_trace()
        renderer_classes = (renderers.JSONRenderer,)
        serializer_class = CustomAuthTokenSerializer
        permission_classes = (AllowAny,)
        email = request.data.get('email')
        password = request.data.get('password')
        # serializer = CustomAuthTokenSerializer(request.data, context={'request':request})
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        # token, _ = Token.objects.get_or_create(user)
        #user = authenticate(request, email=email, password=password)
        user= Doctor.objects.get(email=email)
        if user:
            import pdb;pdb.set_trace()
            from core.signals import  create_auth_token
            token, created = create_auth_token(instance=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class Register(APIView):
    def post(self, request, *args, **kwargs):
        try:
            import pdb;pdb.set_trace()
            response = create_doctor_user(data=request.data)
            # if  request.data['user'] == 'doctor':
            #     response = create_doctor_user(data=request.data)
            # elif  request.data['user'] == 'patient':
            #     response = create_patient_user(data=request.data)
        except Exception as e:
            return Response({"success": False, "message": "Something went wrong","error":e})
        else:
            return Response(response)
    
