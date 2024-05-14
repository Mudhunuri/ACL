from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path as url

#from rest_framework.authtoken import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from core.views import obtain_auth_token
from core.views import Register,ForgotPassword,ResetPassword,ListofDoctors,DemographicsView,GetCurrentPhase, \
DemographicsEditView,DemographicsDoctorView,EditUser,GetPhases,DemographicsDelete,DemographicsGetView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^login/', csrf_exempt(obtain_auth_token)),
    url(r'^register/', Register.as_view()),
    url(r'^forgot_password/', ForgotPassword.as_view()),
    url(r'^reset_password/', ResetPassword.as_view()),
    url(r'^edit_user', EditUser.as_view()),
    url(r'^doctor_list/', ListofDoctors.as_view()),
    #url(r'^create_demographics/', DemographicsView.as_view()),
    url(r'^create_phases/', DemographicsView.as_view()),
    url(r'^get_demographics/', DemographicsGetView.as_view()),
    url(r'^get_phases/', GetPhases.as_view()),
    url(r'^get_current_phase/', GetCurrentPhase.as_view()),
    url(r'^edit_phases/', DemographicsEditView.as_view()),
    url(r'^change_doctor/',DemographicsEditView.as_view()),
    url(r'^doctor_approve/',DemographicsDoctorView.as_view()),
    url(r'^delete_survey/',DemographicsDelete.as_view()),
]

