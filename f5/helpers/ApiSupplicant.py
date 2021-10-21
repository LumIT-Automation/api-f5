from base64 import b64encode
import requests

from django.conf import settings

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException


class ApiSupplicant:
    def __init__(self, endpoint: str, auth: dict, tlsVerify: bool = True, params: dict = None, silent: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.endpoint = endpoint
        self.params = params
        self.tlsVerify = tlsVerify
        self.httpProxy = settings.API_SUPPLICANT_HTTP_PROXY
        self.authorization = "Basic "+b64encode((auth["username"]+":"+auth["password"]).encode()).decode("ascii")
        self.silent = silent

        self.responseStatus = 500
        self.responseObject = dict()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def get(self) -> dict:
        # Fetches the resource from the HTTP REST API endpoint specified.

        # In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception.
        # If a request times out, a Timeout exception is raised.
        # If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
        # SSLError on SSL/TLS error.

        # On KO status codes, a CustomException is raised, with response status and body.

        try:
            # Fetch the remote resource from the F5 backend.
            response = requests.get(self.endpoint,
                proxies=self.httpProxy,
                verify=self.tlsVerify,
                timeout=settings.API_SUPPLICANT_NETWORK_TIMEOUT,

                headers={
                    "Authorization": self.authorization
                },
                params=self.params # GET parameters.
            )

            self.responseStatus = response.status_code

            try:
                self.responseObject = response.json()
            except Exception:
                self.responseObject = {}

            Log.actionLog("Fetching remote: GET "+str(self.endpoint)+" with params: "+str(self.params)) # here for threaded calls.
            Log.actionLog("Remote response HTTP status: "+str(self.responseStatus))

            if not self.silent:
                Log.actionLog("Remote response headers: "+str(response.headers))
                Log.actionLog("Remote response payload: "+str(self.responseObject))
            else:
                Log.actionLog("Remote response headers: silenced by caller.")
                Log.actionLog("Remote response payload: silenced by caller.")

            if self.responseStatus == 200: # ok.
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



    def post(self, data: object, additionalHeaders: dict = {}) -> dict:
        # In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception.
        # If a request times out, a Timeout exception is raised.
        # If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
        # SSLError on SSL/TLS error.

        # On KO status codes, a CustomException is raised, with response status and body.

        standardHeaders = {
            "Authorization": self.authorization
        }

        # Merge headers.
        for k, v in standardHeaders.items():
            if standardHeaders[k] in additionalHeaders:
                standardHeaders[k] = additionalHeaders[k] # additionalHeaders wins on common headers.

        headers = {**standardHeaders, **additionalHeaders} # merge dicts.

        try:
            Log.actionLog("Posting to remote: "+str(self.endpoint))
            Log.actionLog(data)

            response = requests.post(self.endpoint,
                proxies=self.httpProxy,
                verify=self.tlsVerify,
                timeout=settings.API_SUPPLICANT_NETWORK_TIMEOUT,

                headers=headers,
                params=None,
                data=data
            )

            self.responseStatus = response.status_code

            try:
                self.responseObject = response.json()
            except Exception:
                self.responseObject = {}

            Log.actionLog("Remote response status: "+str(self.responseStatus))
            Log.actionLog("Remote response headers: "+str(response.headers))
            Log.actionLog("Remote response payload: "+str(self.responseObject))

            if self.responseStatus == 201 or self.responseStatus == 200: # 201 created + 200 created-for-dummies.
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



    def put(self, data: object, additionalHeaders: dict = {}) -> dict:
        # In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception.
        # If a request times out, a Timeout exception is raised.
        # If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
        # SSLError on SSL/TLS error.

        # On KO status codes, a CustomException is raised, with response status and body.

        standardHeaders = {
            "Authorization": self.authorization
        }

        # Merge headers.
        for k, v in standardHeaders.items():
            if standardHeaders[k] in additionalHeaders:
                standardHeaders[k] = additionalHeaders[k] # additionalHeaders wins on common headers.

        headers = {**standardHeaders, **additionalHeaders} # merge dicts.

        try:
            Log.actionLog("Putting to remote: "+str(self.endpoint))

            response = requests.put(self.endpoint,
                proxies=self.httpProxy,
                verify=self.tlsVerify,
                timeout=settings.API_SUPPLICANT_NETWORK_TIMEOUT,

                headers=headers,
                params=None,
                data=data
            )

            self.responseStatus = response.status_code

            try:
                self.responseObject = response.json()
            except Exception:
                self.responseObject = {}

            Log.actionLog("Remote response status: "+str(self.responseStatus))
            Log.actionLog("Remote response headers: "+str(response.headers))
            Log.actionLog("Remote response payload: "+str(self.responseObject))

            if self.responseStatus == 200: # ok.
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



    def patch(self, data: object, additionalHeaders: dict = {}) -> dict:
        # In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception.
        # If a request times out, a Timeout exception is raised.
        # If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
        # SSLError on SSL/TLS error.

        # On KO status codes, a CustomException is raised, with response status and body.

        standardHeaders = {
            "Authorization": self.authorization
        }

        # Merge headers.
        for k, v in standardHeaders.items():
            if standardHeaders[k] in additionalHeaders:
                standardHeaders[k] = additionalHeaders[k] # additionalHeaders wins on common headers.

        headers = {**standardHeaders, **additionalHeaders} # merge dicts.

        try:
            Log.actionLog("Patching remote: "+str(self.endpoint))

            response = requests.patch(self.endpoint,
                proxies=self.httpProxy,
                verify=self.tlsVerify,
                timeout=settings.API_SUPPLICANT_NETWORK_TIMEOUT,

                headers=headers,
                params=None,
                data=data
            )

            self.responseStatus = response.status_code

            try:
                self.responseObject = response.json()
            except Exception:
                self.responseObject = {}

            Log.actionLog("Remote response status: "+str(self.responseStatus))
            Log.actionLog("Remote response headers: "+str(response.headers))
            Log.actionLog("Remote response payload: "+str(self.responseObject))

            if self.responseStatus == 200: # ok.
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



    def delete(self, additionalHeaders: dict = {}) -> dict:
        # In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception.
        # If a request times out, a Timeout exception is raised.
        # If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
        # SSLError on SSL/TLS error.

        # On KO status codes, a CustomException is raised, with response status and body.

        standardHeaders = {
            "Authorization": self.authorization
        }

        # Merge headers.
        for k, v in standardHeaders.items():
            if standardHeaders[k] in additionalHeaders:
                standardHeaders[k] = additionalHeaders[k] # additionalHeaders wins on common headers.

        headers = {**standardHeaders, **additionalHeaders} # merge dicts.

        try:
            Log.actionLog("Deleting remote: "+str(self.endpoint))

            response = requests.delete(self.endpoint,
                proxies=self.httpProxy,
                verify=self.tlsVerify,
                timeout=settings.API_SUPPLICANT_NETWORK_TIMEOUT,

                headers=headers
            )

            self.responseStatus = response.status_code

            try:
                self.responseObject = response.json()
            except Exception:
                self.responseObject = {}

            Log.actionLog("Remote response status: "+str(self.responseStatus))
            Log.actionLog("Remote response headers: "+str(response.headers))
            Log.actionLog("Remote response payload: "+str(self.responseObject))

            if self.responseStatus == 200: # ok.
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
