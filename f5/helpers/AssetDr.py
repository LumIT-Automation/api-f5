import functools

from django.http import HttpRequest
from rest_framework.request import Request

from f5.models.F5.Asset.Asset import Asset
from f5.helpers.Log import Log

class AssetDr:
    def __init__(self, restCall, *args, **kwargs) -> None:
        self.rest = restCall
        self.prAssetId: int = 0
        self.assets = list() # List of the dr asset ids.


    def __get_dr_assets(self) -> list:
        l = list()
        try:
            if self.prAssetId:
                l = Asset(self.prAssetId).drListIds()

            return l
        except Exception as e:
            raise e



    def __call__(self, request: callable, **kwargs):
        @functools.wraps(request)
        def wrapped():
            # Stack the responses.
            r = list()

            self.prAssetId = int(kwargs["assetId"])
            self.assets = [self.prAssetId] # Todo: call primary asset here, do not enter in loop for primary.
            self.assets.extend(self.__get_dr_assets())

            for assetId in self.assets:
                try:
                    newPath = self.__get_new_path(request.path, assetId)
                    req = AssetDr.__copyRequest__(request, newPath)
                    kwargs["assetId"] = assetId # What the f...

                    r.append(self.rest(req, **kwargs))
                except Exception as e:
                    raise e
            return r[0]

        return wrapped()



    def __get_new_path(self, path: str, assetId: int):
        try:
            return path.replace("/f5/" + str(self.prAssetId) + "/", "/f5/" + str(assetId) + "/")
        except Exception as e:
            raise e



    @staticmethod
    def __copyRequest__(request: Request, path) -> Request:
        try:
            djangoHttpRequest = HttpRequest()
            djangoHttpRequest.GET = request._request.GET.copy()
            djangoHttpRequest.POST = request._request.POST.copy()
            djangoHttpRequest.COOKIES = request._request.COOKIES
            djangoHttpRequest.FILES = request._request.FILES
            djangoHttpRequest.META = request._request.META
            djangoHttpRequest.headers = request._request.headers
            djangoHttpRequest.auth = request._request.auth
            djangoHttpRequest.data = request._request.body
            djangoHttpRequest.user = request._request.user
            djangoHttpRequest.path = path

            req = Request(djangoHttpRequest)
            req.authenticators = request.authenticators

            return req
        except Exception as e:
            raise e
