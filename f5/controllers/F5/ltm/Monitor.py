from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Monitor import Monitor

from f5.serializers.F5.ltm.Monitor import F5MonitorSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update



class F5MonitorController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="monitor", *args, **kwargs)


    def get(self, request: Request, assetId: int, partitionName: str, monitorType: str, monitorName: str) -> Response:
        subPath, name = monitorName.rsplit('~', 1) if '~' in monitorName else ['', monitorName]; subPath = subPath.replace('~', '/')

        return self.getInfo(
            request=request,
            actionCallback=lambda: Monitor(assetId, partitionName, monitorType, name, subPath).info(),
            objectName=monitorName,
            assetId=assetId,
            partitionName=partitionName,
            objectType=monitorType
        )



    def delete(self, request: Request, assetId: int, partitionName: str, monitorType: str, monitorName: str) -> Response:
        subPath, name = monitorName.rsplit('~', 1) if '~' in monitorName else ['', monitorName]; subPath = subPath.replace('~', '/')

        return self.remove(
            request=request,
            actionCallback=lambda: Monitor(assetId, partitionName, monitorType, name, subPath).delete(),
            objectName=monitorName,
            assetId=assetId,
            partitionName=partitionName,
            objectType=monitorType
        )



    def patch(self, request: Request, assetId: int, partitionName: str, monitorType: str, monitorName: str) -> Response:
        subPath, name = monitorName.rsplit('~', 1) if '~' in monitorName else ['', monitorName]; subPath = subPath.replace('~', '/')

        return self.modify(
            request=request,
            actionCallback=lambda data: Monitor(assetId, partitionName, monitorType, name, subPath).modify(data),
            objectName=monitorName,
            assetId=assetId,
            partitionName=partitionName,
            objectType=monitorType,
            Serializer=Serializer
        )
