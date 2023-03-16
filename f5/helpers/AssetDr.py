import functools

from django.http import HttpRequest
from rest_framework.request import Request

from f5.models.F5.Asset.Asset import Asset
from f5.helpers.Log import Log

class AssetDr:
    def __init__(self, restCall, *args, **kwargs) -> None:
        Log.log(restCall, 'RRRRRRRRRRRRRRRRRR')
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



    def __call__(self, request: Request, **kwargs):
        @functools.wraps(request)
        def wrapped():
            # Stack the responses.
            r = list()
            Log.log(request, 'SSSSSSSSSSSSSSSSSSSS')

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
            djangoHttpRequest.query_params = request.query_params.copy()
            djangoHttpRequest.POST = request.POST.copy()
            djangoHttpRequest.data = request.data
            djangoHttpRequest.FILES = request.FILES
            djangoHttpRequest.auth = request.auth
            djangoHttpRequest.META = request.META
            req = Request(djangoHttpRequest)
            req.authenticators = request.authenticators

            req.accepted_media_type = request.accepted_media_type
            req.accepted_renderer = request.accepted_renderer
            req.version = request.version
            req.versioning_scheme = request.versioning_scheme

            Log.log(dir(request), 'DDDDDDDDDDDDD')
            Log.log(dir(djangoHttpRequest), 'JJJJJJJJJJJJJJJJ')
            Log.log(dir(req), 'RRRRRRRRRRRRRR')
            return req
        except Exception as e:
            raise e
