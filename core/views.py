from rest_framework.views import APIView
import json
from drf_spectacular.utils import extend_schema, inline_serializer
from django.http import HttpResponse
from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import CharField, EmailField
from .authentication import expires_in, token_expire_handler, ExpiringTokenAuthentication
from .constants import DOCTOR_ADMIN, PATIENT_ADMIN
from .serializer import CustomAuthTokenSerializer
from .helper import reset_password_notification,create_doctor_user,create_patient_user, \
    get_user_from_email,reset_password

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

        val = {'token': token.key, 'token_expires_in': str(time_left),'first_name': user.first_name, 'last_name': user.last_name}

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
        
class Register(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        
        try:
            #response = create_doctor_user(data=request.data)
            if  request.data['role'] == 'doctor':
                response = create_doctor_user(data=request.data)
            elif  request.data['role'] == 'patient':
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
        role = request.data.get('role')
        print(request)
        if email is not None:
            print("not none")
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
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
