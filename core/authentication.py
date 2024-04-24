from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from datetime import timedelta
from django.utils import timezone
from django.conf import settings

def expires_in(token):
    '''
    this function returns left time to expire token
    '''
    time_elapsed = timezone.now() - token.created
    token_expiration_timer = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return token_expiration_timer

def is_token_expired(token):
    '''
    checks whether token is expired or not
    '''
    return expires_in(token) < timedelta(seconds = 0)


def token_expire_handler(token):
    '''
    checks whether token is active or not.
    If token is expired deletes the old token and creates the new one.
    '''
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user = token.user)
    return is_expired, token