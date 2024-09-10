from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Node import Node

from f5.serializers.F5.ltm.Nodes import F5NodesSerializer as NodesSerializer
from f5.serializers.F5.ltm.Node import F5NodeSerializer as NodeSerializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList
from f5.controllers.CustomControllerPost import CustomControllerF5Create


class F5NodesController(CustomControllerF5GetList, CustomControllerF5Create):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="node", *args, **kwargs)



    def get(self, request: Request, assetId: int, partitionName: str) -> Response:

        return self.getList(
            request=request,
            actionCallback=lambda:  Node.dataList(assetId, partitionName),
            assetId=assetId,
            partition=partitionName,
            Serializer=NodesSerializer,
        )



    def post(self, request: Request, assetId: int, partitionName: str) -> Response:
        def dataFix(data: dict):
            data["partition"] = partitionName
            if "state" in data:
                data["State"] = data["state"]  # curious F5 field's name.
                del (data["state"])

            return data


        return self.create(
            request=request,
            actionCallback=lambda data: Node.add(assetId, data),
            assetId=assetId,
            partition=partitionName,
            Serializer=NodeSerializer,
            lockItemField="name",
            dataFix=dataFix
        )
