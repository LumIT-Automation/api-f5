from typing import List

from django.http import HttpRequest
from rest_framework.request import Request

from f5.models.F5.Asset.Asset import Asset


class ReplicateVirtualServerBase:
    def __init__(self, wrappedMethod: callable, *args, **kwargs) -> None:
        self.wrappedMethod = wrappedMethod
        self.request = None
        self.primaryAssetId: int = 0
        self.primaryPartitionName: str = ""



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def __call__(self, request: Request, **kwargs):
        raise NotImplementedError



    ####################################################################################################################
    # Protected methods
    ####################################################################################################################

    def _listAssetsDr(self) -> List[dict]:
        l = list()

        try:
            if self.primaryAssetId:
                l = Asset(self.primaryAssetId).drDataList(onlyEnabled=True)

            return l
        except Exception as e:
            raise e



    ####################################################################################################################
    # Protected static methods
    ####################################################################################################################

    @staticmethod
    def _forgeRequest(request: Request, additionalQueryParams: dict = None) -> Request:
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
