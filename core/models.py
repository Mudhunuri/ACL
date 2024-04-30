from django.db import models
from django.utils.translation import gettext_lazy as _
from core.manager import ActiveUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import JSONField
from core.constants import DoctorApproval

class BaseUser(AbstractBaseUser):
    is_active = models.BooleanField(_('active'),default=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    experience = models.IntegerField(null=True)
    phone = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=100, blank=True)
    degree = models.CharField(max_length=15,blank=True,null=True)  # Note: You might want to use Django's built-in password field for security
    objects=ActiveUserManager()
    role=models.CharField(max_length=50, blank=True)
    license=models.CharField(max_length=50, blank=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Demographics(models.Model):
    country = models.CharField(max_length=100, blank=True,null=True)
    gender = models.CharField(max_length=50, blank=True,null=True)
    dob = models.DateField(null=True,blank=True)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    sport = models.CharField(max_length=200, blank=True,null=True)
    current_activity = models.CharField(max_length=1000, blank=True,null=True)
    date_of_injury = models.DateField(null=True,blank=True)
    knee = models.CharField(max_length=50, blank=True,null=True)
    mechanism_injury = models.CharField(max_length=1000,null=True, blank=True)
    other_injuries = models.CharField(max_length=4000,null=True, blank=True)
    injuries_same = models.IntegerField(null=True)
    injuries_other = models.IntegerField(null=True)
    reconstructions_same = models.IntegerField(null=True)
    reconstructions_other = models.IntegerField(null=True)
    planned_management = models.CharField(max_length=500,blank=True,null=True)
    survey_date = models.DateTimeField(null=True,blank=True)
    patient = models.ForeignKey(BaseUser,on_delete=models.CASCADE, null=True, blank=True,related_name='+')
    doctor = models.ForeignKey(BaseUser,on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    doctors_history = JSONField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True,default=DoctorApproval.OPEN)
    #doctor_accepted = models.BooleanField(default=False, null=True,default=DoctorApproval.OPEN)
    percentage = models.IntegerField(null=True)
    draft = models.BooleanField(default=True)

