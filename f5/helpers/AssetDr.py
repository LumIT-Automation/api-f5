import functools

from django.http import HttpRequest
from rest_framework.request import Request

from f5.models.F5.Asset.Asset import Asset
from f5.helpers.Log import Log

class AssetDr:
    def __init__(self, wrappedMethod: callable, *args, **kwargs) -> None:
        self.wrappedMethod = wrappedMethod
        self.primaryAssetId: int = 0
        self.assets = list() # List of the dr asset ids.



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def __call__(self, request: Request, **kwargs):
        @functools.wraps(request)
        def wrapped():
            ENABLE_DR = 1
            responses = list()

            # Perform the request to the primary asset.
            result = self.wrappedMethod(request, **kwargs)
            responses.append(result)

            if ENABLE_DR:
                self.primaryAssetId = int(kwargs["assetId"])
                for assetId in self.__get_dr_assets():
                    try:
                        newPath = self.__get_new_path(request.path, assetId)
                        req = AssetDr.__copyRequest(request, newPath)
                        kwargs["assetId"] = assetId

                        responses.append(self.wrappedMethod(req, **kwargs))
                    except Exception as e:
                        raise e
            return responses[0]

        return wrapped()



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __get_dr_assets(self) -> list:
        l = list()
        try:
            if self.primaryAssetId:
                l = Asset(self.primaryAssetId).drListIds()

            return l
        except Exception as e:
            raise e



    def __get_new_path(self, path: str, assetId: int):
        try:
            return path.replace("/f5/" + str(self.primaryAssetId) + "/", "/f5/" + str(assetId) + "/")
        except Exception as e:
            raise e



    @staticmethod
    def __copyRequest(request: Request, path) -> Request:
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
