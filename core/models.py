# from django.core import validators
# from django.db import models
# from django.contrib.auth.models import User
# from core.constants import DOCTOR_ADMIN,PATIENT_ADMIN

# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.db import models

# class Doctor(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     experience = models.IntegerField()
#     phone = models.CharField(max_length=15)
#     password = models.CharField(max_length=100)
#     degree = models.CharField(max_length=15,blank=True)  # Note: You might want to use Django's built-in password field for security

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['email']

#     def __str__(self):
#         return self.email

# class PatientUser(models.Model):
#     """
#     Adcuser keeps all the adcuratio user information. This model
#     is related to :class:`Agency` , :class:`Company`,
#     :class:`Brand` , :class:`Channel`
#     """
#     # first name of the user.
#     first_name = models.CharField(max_length=250, blank=True)
#     # last name of the user.
#     last_name = models.CharField(max_length=250, blank=True)
#     # email of the user.
#     email = models.EmailField(unique=True, blank=True)
#     phone = models.CharField(blank=True, null=True,max_length=15)
#     password = models.CharField(max_length=250)
#     #objects = ActiveUserManager()