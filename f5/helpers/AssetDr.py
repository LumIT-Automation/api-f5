import functools

from django.http import HttpRequest
from rest_framework.request import Request

from f5.models.F5.Asset.Asset import Asset
from f5.helpers.Log import Log

class AssetDr:
    def __init__(self, wrappedMethod: callable, *args, **kwargs) -> None:
        self.wrappedMethod = wrappedMethod
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
            ENABLE_DR = 1
            responses = list()

            # Perform the request to the primary asset.
            result = self.wrappedMethod(request, **kwargs)
            responses.append(result)

            if ENABLE_DR:
                self.prAssetId = int(kwargs["assetId"])
                self.assets = self.__get_dr_assets()

                for assetId in self.assets:
                    try:
                        newPath = self.__get_new_path(request.path, assetId)
                        req = AssetDr.__copyRequest__(request, newPath)
                        kwargs["assetId"] = assetId

                        responses.append(self.wrappedMethod(req, **kwargs))
                    except Exception as e:
                        raise e
            return responses[0]

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
            for attr in ("POST", "data", "FILES", "auth", "META"):
                setattr(djangoHttpRequest, attr, getattr(request, attr))

            req = Request(djangoHttpRequest)
            for attr in ("authenticators", "accepted_media_type", "accepted_renderer", "version", "versioning_scheme"):
                setattr(req, attr, getattr(request, attr))

            return req
        except Exception as e:
            raise e
