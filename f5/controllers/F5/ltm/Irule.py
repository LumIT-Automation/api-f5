from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Irule import Irule

from f5.serializers.F5.ltm.Irule import F5IruleSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update



class F5IruleController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="irule", *args, **kwargs)


    def get(self, request: Request, assetId: int, partitionName: str, iruleName: str) -> Response:
        subPath, name = iruleName.rsplit('~', 1) if '~' in iruleName else ['', iruleName]; subPath = subPath.replace('~', '/')

        return self.getInfo(
            request=request,
            actionCallback=lambda: Irule(assetId, partitionName, name, subPath).info(),
            objectName=iruleName,
            assetId=assetId,
            partitionName=partitionName
        )



    def delete(self, request: Request, assetId: int, partitionName: str, iruleName: str) -> Response:
        subPath, name = iruleName.rsplit('~', 1) if '~' in iruleName else ['', iruleName]; subPath = subPath.replace('~', '/')

        return self.remove(
            request=request,
            actionCallback=lambda: Irule(assetId, partitionName, name, subPath).delete(),
            objectName=iruleName,
            assetId=assetId,
            partitionName=partitionName
        )



    def patch(self, request: Request, assetId: int, partitionName: str, iruleName: str) -> Response:
        subPath, name = iruleName.rsplit('~', 1) if '~' in iruleName else ['', iruleName]; subPath = subPath.replace('~', '/')

        return self.modify(
            request=request,
            actionCallback=lambda data: Irule(assetId, partitionName, name, subPath).modify(data),
            objectName=iruleName,
            assetId=assetId,
            partitionName=partitionName,
            Serializer=Serializer
        )
