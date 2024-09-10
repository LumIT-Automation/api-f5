from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Pool import Pool

from f5.serializers.F5.ltm.Pools import F5PoolsSerializer as PoolsSerializer
from f5.serializers.F5.ltm.Pool import F5PoolSerializer as PoolSerializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList
from f5.controllers.CustomControllerPost import CustomControllerF5Create


class F5PoolsController(CustomControllerF5GetList, CustomControllerF5Create):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="pool", *args, **kwargs)



    def get(self, request: Request, assetId: int, partitionName: str) -> Response:

        return self.getList(
            request=request,
            actionCallback=lambda: Pool.dataList(assetId, partitionName),
            assetId=assetId,
            partition=partitionName,
            Serializer=PoolsSerializer
        )



    def post(self, request: Request, assetId: int, partitionName: str) -> Response:
        def dataFix(data: dict):
            data["partition"] = partitionName
            return data


        return self.create(
            request=request,
            actionCallback=lambda data: Pool.add(assetId, data),
            assetId=assetId,
            partition=partitionName,
            Serializer=PoolSerializer,
            lockItemField="name",
            dataFix=dataFix,
        )
