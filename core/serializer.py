from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
#from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .model.base_models import Doctor


class CustomAuthTokenSerializer(AuthTokenSerializer):
    email = serializers.CharField(label=_("email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')
        import pdb;pdb.set_trace()
        if username and password:
            check=False
            user = Doctor.objects.get(email=username)
            if check_password(password,user.password):
                check=True
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not check:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

# class UpdatePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)

#     # noinspection PyMethodMayBeStatic
#     def validate_new_password(self, value):
#         validate_password(value)
#         return value

