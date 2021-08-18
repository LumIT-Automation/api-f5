import jwt

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from f5.helpers.Log import Log


class CustomController(APIView):
    if not settings.DISABLE_AUTHENTICATION:
        permission_classes = [IsAuthenticated]
        authentication_classes = [JWTTokenUserAuthentication]



    @staticmethod
    def loggedUser(request: Request) -> dict:
        if settings.DISABLE_AUTHENTICATION:
            user = {
                "authDisabled": True,
                "groups": []
            }
        else:
            # Retrieve user from the JWT token.
            authenticator = request.successful_authenticator
            user = jwt.decode(
                authenticator.get_raw_token(authenticator.get_header(request)),
                settings.SIMPLE_JWT['VERIFYING_KEY'],
                settings.SIMPLE_JWT['ALGORITHM'],
                do_time_check=True
            )
            user["authDisabled"] = False

        return user



    @staticmethod
    def exceptionHandler(e: Exception) -> tuple:
        Log.logException(e)

        data = dict()
        headers = { "Cache-Control": "no-cache" }

        if any(exc in e.__class__.__name__ for exc in ("ConnectionError", "Timeout", "TooManyRedirects", "SSLError", "HTTPError")):
            httpStatus = status.HTTP_503_SERVICE_UNAVAILABLE
            data["error"] = {
                "network": e.__str__()
            }
        elif e.__class__.__name__ == "CustomException":
            httpStatus = e.status
            data["error"] = e.payload
        else:
            data = None
            httpStatus = status.HTTP_500_INTERNAL_SERVER_ERROR # generic.

        return data, httpStatus, headers
