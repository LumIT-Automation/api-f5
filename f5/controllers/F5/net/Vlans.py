from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.net.Vlan import Vlan

from f5.serializers.F5.net.Vlans import F5VlansSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList


class F5VlansController(CustomControllerF5GetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="vlan", *args, **kwargs)



    def get(self, request: Request, assetId: int) -> Response:

        return self.getList(
            request=request,
            actionCallback=lambda: Vlan.dataList(assetId),
            assetId=assetId,
            Serializer=Serializer
        )
