from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.SnatPool import SnatPool

from f5.serializers.F5.ltm.SnatPool import F5SnatPoolSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update


class F5SnatPoolController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="snatPool", *args, **kwargs)


    def get(self, request: Request, assetId: int, partitionName: str, snatPoolName: str) -> Response:
        subPath, name = snatPoolName.rsplit('~', 1) if '~' in snatPoolName else ['', snatPoolName]; subPath = subPath.replace('~', '/')

        return self.getInfo(
            request=request,
            actionCallback=lambda: SnatPool(assetId, partitionName, name, subPath).info(),
            objectName=snatPoolName,
            assetId=assetId,
            partitionName=partitionName
        )



    def delete(self, request: Request, assetId: int, partitionName: str, snatPoolName: str) -> Response:
        subPath, name = snatPoolName.rsplit('~', 1) if '~' in snatPoolName else ['', snatPoolName]; subPath = subPath.replace('~', '/')

        return self.remove(
            request=request,
            actionCallback=lambda: SnatPool(assetId, partitionName, name, subPath).delete(),
            objectName=snatPoolName,
            assetId=assetId,
            partitionName=partitionName
        )



    def patch(self, request: Request, assetId: int, partitionName: str, snatPoolName: str) -> Response:
        subPath, name = snatPoolName.rsplit('~', 1) if '~' in snatPoolName else ['', snatPoolName]; subPath = subPath.replace('~', '/')

        return self.modify(
            request=request,
            actionCallback=lambda data:  SnatPool(assetId, partitionName, name, subPath).modify(data),
            objectName=snatPoolName,
            assetId=assetId,
            partitionName=partitionName,
            Serializer=Serializer
        )
