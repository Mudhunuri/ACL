from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path as url

#from rest_framework.authtoken import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from core.views import obtain_auth_token
from core.views import Register,Login
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^login/', csrf_exempt(obtain_auth_token)),
    url(r'^register/', Register.as_view()),
    # url(r'^forgot_password/', ForgotPassword.as_view()),
    # url(r'^reset_auth/', ResetAuth.as_view()),
    # url(r'^reset_password/', ResetPassword.as_view()),
    # url(r'^update_password/', UpdatePassword.as_view()),  
]
