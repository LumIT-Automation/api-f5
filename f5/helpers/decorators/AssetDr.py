import uuid
import functools

from django.conf import settings
from django.http import HttpRequest
from rest_framework.request import Request

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.Log import Log


if not hasattr(settings, "ENABLE_ASSET_DR") or not settings.ENABLE_ASSET_DR:
    def AssetDr(func): # null decorator.
        return func
else:
    class AssetDr:
        def __init__(self, wrappedMethod: callable, *args, **kwargs) -> None:
            self.wrappedMethod = wrappedMethod
            self.primaryAssetId: int = 0
            self.assets = list() # dr asset ids list.



        ####################################################################################################################
        # Public methods
        ####################################################################################################################

        def __call__(self, request: Request, **kwargs):
            @functools.wraps(request)
            def wrapped():
                try:
                    relationUuid = uuid.uuid4().hex
                    self.primaryAssetId = int(kwargs["assetId"])

                    # Modify the request injecting the __concertoDrReplicaFlow query parameter,
                    # then perform the request to the primary asset.
                    responsePr = self.wrappedMethod(
                        AssetDr.__forgeRequest(
                            request=request,
                            additionalQueryParams={"__concertoDrReplicaFlow": relationUuid}
                        ),
                        **kwargs
                    )

                    if responsePr.status_code in (200, 201, 202, 204): # reply the action in dr only if it was successful.
                        if "dr" in request.query_params and request.query_params["dr"]: # reply action in dr only if dr=1 param was passed.
                            for asset in self.__listAssetsDr():
                                try:
                                    # Modify the request injecting the dr asset and the __concertoDrReplicaFlow query parameter,
                                    # then re-run the decorated method.
                                    req = AssetDr.__forgeRequest(
                                        request=request,
                                        additionalQueryParams={"__concertoDrReplicaFlow": relationUuid}
                                    )
                                    kwargs["assetId"] = asset.get("id", 0)

                                    self.wrappedMethod(req, **kwargs)
                                except Exception as e:
                                    raise e

                    return responsePr
                except Exception as e:
                    raise e

            return wrapped()



        ####################################################################################################################
        # Private methods
        ####################################################################################################################

        def __listAssetsDr(self) -> list:
            l = list()

            try:
                if self.primaryAssetId:
                    l = Asset(self.primaryAssetId).drDataList(onlyEnabled=True)

                return l
            except Exception as e:
                raise e



        ####################################################################################################################
        # Private static methods
        ####################################################################################################################

        @staticmethod
        def __forgeRequest(request: Request, additionalQueryParams: dict = None) -> Request:
            additionalQueryParams = additionalQueryParams or {}

            try:
                djangoHttpRequest = HttpRequest()
                djangoHttpRequest.path = request.path[:]
                djangoHttpRequest.method = request.method
                query_params = request.query_params.copy()
                if "dr" in query_params:
                    del query_params["dr"]

                if additionalQueryParams:
                    query_params.update(additionalQueryParams)

                for attr in ("POST", "data", "FILES", "auth", "META"):
                    setattr(djangoHttpRequest, attr, getattr(request, attr))

                req = Request(djangoHttpRequest)
                for attr in ("authenticators", "accepted_media_type", "accepted_renderer", "version", "versioning_scheme"):
                    setattr(req, attr, getattr(request, attr))

                if additionalQueryParams:
                    req.query_params.update(query_params)

                return req
            except Exception as e:
                raise e
