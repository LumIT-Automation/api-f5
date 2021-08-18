import logging
from django.http import request, response


class LogMiddleware:
    def __init__(self, response: response) -> None:
        self.response = response
        self.log = logging.getLogger("http") # setup LOGGING in settings.py



    def __call__(self, request: request) -> response:
        self.log.debug("Request: "+str(request))

        response = self.response(request)
        return response
