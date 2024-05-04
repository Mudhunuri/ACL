from django.db import models
from django.utils.translation import gettext_lazy as _
from core.manager import ActiveUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models import JSONField
from core.constants import DoctorApproval,Phases

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
    current_phase= models.CharField(max_length=50,default=Phases.DEMOGRAPHICS)

class PreOp(models.Model):
    demographics = models.ForeignKey(Demographics,on_delete=models.CASCADE, null=True, blank=True)
    date =  models.DateField(null=True,blank=True)
    passive_extension = models.IntegerField(null=True)
    passive_flexion = models.IntegerField(null=True)
    swelling = models.CharField(max_length=50, blank=True,null=True)
    dynamometer_affected = models.IntegerField(null=True)
    dynamometer_non_affected = models.IntegerField(null=True)
    dynamometer_symmetry = models.FloatField(null=True)
    hop_trial_1 = models.IntegerField(null=True)
    hop_trial_2 = models.IntegerField(null=True)
    hop_symmetry = models.IntegerField(null=True)
    percentage = models.FloatField(null=True)
    draft = models.BooleanField(default=True)

class Phase1(models.Model):
    Demographics = models.ForeignKey(Demographics,on_delete=models.CASCADE, null=True, blank=True)
    date =  models.DateField(null=True,blank=True)
    date_of_surgery = models.DateField(null=True,blank=True)
    graft = models.CharField(max_length=50, blank=True,null=True)
    passive_extension = models.IntegerField(null=True)
    passive_flexion = models.IntegerField(null=True)
    swelling = models.CharField(max_length=50, blank=True,null=True)
    quads = models.IntegerField(null=True)
    percentage = models.IntegerField(null=True)
    draft = models.BooleanField(default=True)

class Phase2(models.Model):
    Demographics = models.ForeignKey(Demographics,on_delete=models.CASCADE, null=True, blank=True)
    percentage = models.IntegerField(null=True)
    draft = models.BooleanField(default=True)
    date =  models.DateField(null=True,blank=True)
    prone_hang = models.IntegerField(null=True)
    passive_flexion = models.IntegerField(null=True)
    swelling = models.CharField(max_length=50, blank=True,null=True)
    functional_alignment = models.CharField(max_length=50, blank=True,null=True)
    bridge_affected = models.IntegerField(null=True)
    bridge_non_affected = models.IntegerField(null=True)
    bridge_hurdle = models.CharField(max_length=50, blank=True,null=True)
    bridge_symmetry = models.FloatField(null=True)
    calf_affected = models.IntegerField(null=True)
    calf_non_affected = models.IntegerField(null=True)
    calf_hurdle = models.CharField(max_length=50, blank=True,null=True)
    calf_symmetry = models.FloatField(null=True)
    endurance_affected = models.IntegerField(null=True)
    endurance_non_affected = models.IntegerField(null=True)
    endurance_hurdle = models.CharField(max_length=50, blank=True,null=True)
    endurance_symmetry = models.FloatField(null=True)
    leg_rise_affected = models.IntegerField(null=True)
    leg_rise_non_affected = models.IntegerField(null=True)
    leg_rise_hurdle = models.CharField(max_length=50, blank=True,null=True)
    leg_rise_symmetry = models.FloatField(null=True)
    unipedal_open_affected=models.IntegerField(null=True)
    unipedal_closed_affected = models.IntegerField(null=True)
    unipedal_open_non_affected=models.IntegerField(null=True)
    unipedal_closed_non_affected = models.IntegerField(null=True)
    unipedal_affected_hurdel = models.CharField(max_length=50, blank=True,null=True)
    unipedal_non_affected_hurdel = models.CharField(max_length=50, blank=True,null=True)
    weight = models.FloatField(null=True)
    leg_press_affected = models.IntegerField(null=True)
    leg_press_affected_weight = models.FloatField(null=True)
    leg_press_non_affected = models.IntegerField(null=True)
    leg_press_non_affected_weight = models.FloatField(null=True)
    squat = models.IntegerField(null=True)
    squat_weight = models.FloatField(null=True)
    





