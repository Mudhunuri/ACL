from rest_framework import status
from rest_framework.response import Response


class BaseApiMixin(object):
    def success_response(self, message="", status_code=status.HTTP_200_OK):
        return Response(message, status=status_code)
    
    def error_response(self, message="", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(message, status=status_code)