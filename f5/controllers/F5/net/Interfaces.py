from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.net.Interface import Interface

from f5.serializers.F5.net.Vlans import F5VlansSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList


class F5InterfacesController(CustomControllerF5GetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="interface", *args, **kwargs)



    def get(self, request: Request, assetId: int) -> Response:

        return self.getList(
            request=request,
            actionCallback=lambda: Interface.dataList(assetId),
            assetId=assetId,
            Serializer=Serializer
        )

