from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.SnatPool import SnatPool

from f5.serializers.F5.ltm.SnatPools import F5SnatPoolsSerializer as SnatPoolsSerializer
from f5.serializers.F5.ltm.SnatPool import F5SnatPoolSerializer as SnatPoolSerializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList
from f5.controllers.CustomControllerPost import CustomControllerF5Create



class F5SnatPoolsController(CustomControllerF5GetList, CustomControllerF5Create):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="snatPool", *args, **kwargs)



    def get(self, request: Request, assetId: int, partitionName: str) -> Response:

        return self.getList(
            request=request,
            actionCallback=lambda: SnatPool.dataList(assetId, partitionName),
            assetId=assetId,
            partition=partitionName,
            Serializer=SnatPoolsSerializer
        )



    def post(self, request: Request, assetId: int, partitionName: str) -> Response:
        def dataFix(data: dict):
            data["partition"] = partitionName
            return data


        return self.create(
            request=request,
            actionCallback=lambda data: SnatPool.add(assetId, data),
            assetId=assetId,
            partition=partitionName,
            Serializer=SnatPoolSerializer,
            lockItemField="name",
            dataFix=dataFix,
        )
