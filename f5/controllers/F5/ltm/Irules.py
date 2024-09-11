from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Irule import Irule

from f5.serializers.F5.ltm.Irules import F5IrulesSerializer as IrulesSerializer
from f5.serializers.F5.ltm.Irule import F5IruleSerializer as IruleSerializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList
from f5.controllers.CustomControllerPost import CustomControllerF5Create


class F5IrulesController(CustomControllerF5GetList, CustomControllerF5Create):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="irule", *args, **kwargs)



    def get(self, request: Request, assetId: int, partitionName: str) -> Response:

        return self.getList(
            request=request,
            actionCallback=lambda: Irule.dataList(assetId, partitionName),
            assetId=assetId,
            partitionName=partitionName,
            Serializer=IrulesSerializer
        )



    def post(self, request: Request, assetId: int, partitionName: str) -> Response:
        def dataFix(data: dict):
            data["partition"] = partitionName
            return data


        return self.create(
            request=request,
            actionCallback=lambda data: Irule.add(assetId, data),
            assetId=assetId,
            partitionName=partitionName,
            Serializer=IruleSerializer,
            lockItemDataKey="name",
            dataFix=dataFix,
        )
