from django.db import models
from django.utils.translation import gettext_lazy as _
from core.model.manager import ActiveUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

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
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
