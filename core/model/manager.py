from django.contrib.auth.models import UserManager
class ActiveUserManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().exclude(is_active=False)