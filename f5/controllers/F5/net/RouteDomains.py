from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.net.RouteDomain import RouteDomain

from f5.serializers.F5.net.RouteDomains import F5RouteDomainsSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList


class F5RouteDomainsController(CustomControllerF5GetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="routedomain", *args, **kwargs)



    def get(self, request: Request, assetId: int) -> Response:

        return self.getList(
            request=request,
            actionCallback=lambda: RouteDomain.dataList(assetId),
            assetId=assetId,
            Serializer=Serializer
        )
