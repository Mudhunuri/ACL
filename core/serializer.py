from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
#from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from core.models import BaseUser


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
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include email and password.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

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

