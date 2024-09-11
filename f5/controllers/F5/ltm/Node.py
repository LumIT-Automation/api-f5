from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Node import Node

from f5.serializers.F5.ltm.Node import F5NodeSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update


class F5NodeController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="node", *args, **kwargs)


    def get(self, request: Request, assetId: int, partitionName: str, nodeName: str) -> Response:
        subPath, name = nodeName.rsplit('~', 1) if '~' in nodeName else ['', nodeName]; subPath = subPath.replace('~', '/')

        return self.getInfo(
            request=request,
            actionCallback=lambda: Node(assetId, partitionName, name, subPath).info(),
            objectName=nodeName,
            assetId=assetId,
            partitionName=partitionName
        )



    def delete(self, request: Request, assetId: int, partitionName: str, nodeName: str) -> Response:
        subPath, name = nodeName.rsplit('~', 1) if '~' in nodeName else ['', nodeName]; subPath = subPath.replace('~', '/')

        return self.remove(
            request=request,
            actionCallback=lambda: Node(assetId, partitionName, name, subPath).delete(),
            objectName=nodeName,
            assetId=assetId,
            partitionName=partitionName
        )



    def patch(self, request: Request, assetId: int, partitionName: str, nodeName: str) -> Response:
        subPath, name = nodeName.rsplit('~', 1) if '~' in nodeName else ['', nodeName]; subPath = subPath.replace('~', '/')

        return self.modify(
            request=request,
            actionCallback=lambda data: Node(assetId, partitionName, name, subPath).modify(data),
            objectName=nodeName,
            assetId=assetId,
            partitionName=partitionName,
            Serializer=Serializer
        )
