from typing import Callable
from base64 import b64encode
import requests

from django.conf import settings

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException


class ApiSupplicant:
    def __init__(self, endpoint: str, auth: tuple, tlsVerify: bool = True, params: dict = None, silent: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.endpoint = endpoint
        self.params = params
        self.tlsVerify = tlsVerify
        self.httpProxy = settings.API_SUPPLICANT_HTTP_PROXY
        self.authorization = "Basic "+b64encode((auth[0]+":"+auth[1]).encode()).decode("ascii")
        self.silent = silent

        self.responseStatus = 500
        self.responseObject = dict()
        self.responseHeaders = dict()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def get(self) -> dict:
        try:
            Log.actionLog(
                "[API Supplicant] Fetching remote: GET "+str(self.endpoint)+" with params: "+str(self.params)
            )

            return self.__request(requests.get, params=self.params)
        except Exception as e:
            raise e



    def post(self, data: str, additionalHeaders: dict = None) -> dict:
        additionalHeaders = {} if additionalHeaders is None else additionalHeaders

        try:
            Log.actionLog("[API Supplicant] Posting to remote: "+str(self.endpoint))
            Log.actionLog("[API Supplicant] Posting data: "+str(data))

            return self.__request(requests.post, additionalHeaders=additionalHeaders, data=data)
        except Exception as e:
            raise e



    def put(self, data: str, additionalHeaders: dict = None) -> dict:
        additionalHeaders = {} if additionalHeaders is None else additionalHeaders

        try:
            Log.actionLog(
                "[API Supplicant] Putting to remote: "+str(self.endpoint)
            )

            return self.__request(requests.put, additionalHeaders=additionalHeaders, data=data)
        except Exception as e:
            raise e



    def patch(self, data: str, additionalHeaders: dict = None) -> dict:
        additionalHeaders = {} if additionalHeaders is None else additionalHeaders

        try:
            Log.actionLog(
                "[API Supplicant] Patching remote: "+str(self.endpoint)
            )

            return self.__request(requests.patch, additionalHeaders=additionalHeaders, data=data)
        except Exception as e:
            raise e



    def delete(self) -> dict:
        try:
            Log.actionLog(
                "[API Supplicant] Deleting remote: "+str(self.endpoint)
            )

            return self.__request(requests.delete)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __request(self, request: Callable, additionalHeaders: dict = None, params: dict = None, data: str = ""):
        params = {} if params is None else params
        additionalHeaders = {} if additionalHeaders is None else additionalHeaders

        # In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception.
        # If a request times out, a Timeout exception is raised.
        # If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
        # SSLError on SSL/TLS error.

        # On KO status codes, a CustomException is raised, with response status and body.

        headers = {
            "Authorization": self.authorization
        }

        headers.update(additionalHeaders)

        try:
            response = request(self.endpoint,
                proxies=self.httpProxy,
                verify=self.tlsVerify,
                timeout=settings.API_SUPPLICANT_NETWORK_TIMEOUT,
                headers=headers,
                params=params, # GET parameters.
                data=data
            )

            self.responseStatus = response.status_code
            self.responseHeaders = response.headers

            try:
                self.responseObject = response.json()
            except Exception:
                self.responseObject = {}

            if not self.silent:
                Log.actionLog("[API Supplicant] Remote response status: "+str(self.responseStatus))
                Log.actionLog("[API Supplicant] Remote response headers: "+str(self.responseHeaders))
                Log.actionLog("[API Supplicant] Remote response payload: "+str(self.responseObject))
            else:
                Log.actionLog("[API Supplicant] Remote response silenced by caller.")

            if self.responseStatus == 200 or self.responseStatus == 201: # ok / ok on POST.
                pass
            elif self.responseStatus == 401:
                raise CustomException(status=400, payload={"F5": "Wrong credentials for the asset."})
            else:
                if "message" in self.responseObject:
                    f5Error = self.responseObject["message"]
                else:
                    f5Error = self.responseObject

                raise CustomException(status=self.responseStatus, payload={"F5": f5Error})
        except Exception as e:
            raise e

        return self.responseObject
