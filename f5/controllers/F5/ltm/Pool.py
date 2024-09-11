from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Pool import Pool

from f5.serializers.F5.ltm.Pool import F5PoolSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update


class F5PoolController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="pool", *args, **kwargs)


    def get(self, request: Request, assetId: int, partitionName: str, poolName: str) -> Response:
        subPath, name = poolName.rsplit('~', 1) if '~' in poolName else ['', poolName]; subPath = subPath.replace('~', '/')

        return self.getInfo(
            request=request,
            actionCallback=lambda: Pool(assetId, partitionName, name, subPath).info(),
            objectName=poolName,
            assetId=assetId,
            partitionName=partitionName
        )



    def delete(self, request: Request, assetId: int, partitionName: str, poolName: str) -> Response:
        subPath, name = poolName.rsplit('~', 1) if '~' in poolName else ['', poolName]; subPath = subPath.replace('~', '/')

        return self.remove(
            request=request,
            actionCallback=lambda: Pool(assetId, partitionName, name, subPath).delete(),
            objectName=poolName,
            assetId=assetId,
            partitionName=partitionName
        )



    def patch(self, request: Request, assetId: int, partitionName: str, poolName: str) -> Response:
        subPath, name = poolName.rsplit('~', 1) if '~' in poolName else ['', poolName]; subPath = subPath.replace('~', '/')

        return self.modify(
            request=request,
            actionCallback=lambda data:  Pool(assetId, partitionName, name, subPath).modify(data),
            objectName=poolName,
            assetId=assetId,
            partitionName=partitionName,
            Serializer=Serializer
        )
