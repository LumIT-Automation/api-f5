from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.net.Self import Self

from f5.serializers.F5.net.Selfs import F5SelfsSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList


class F5SelfsController(CustomControllerF5GetList):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="self", *args, **kwargs)



    def get(self, request: Request, assetId: int) -> Response:

        return self.getList(
            request=request,
            actionCallback=lambda: Self.dataList(assetId),
            assetId=assetId,
            Serializer=Serializer
        )
