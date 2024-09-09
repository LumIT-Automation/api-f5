from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Datagroup import Datagroup

from f5.serializers.F5.ltm.Datagroups import F5DatagroupSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update


class F5DatagroupController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="datagroup", *args, **kwargs)


    def delete(self, request: Request, assetId: int, partitionName: str, datagroupType: str, datagroupName: str) -> Response:
        subPath, name = datagroupName.rsplit('~', 1) if '~' in datagroupName else ['', datagroupName]; subPath = subPath.replace('~', '/')

        return self.remove(
            request=request,
            actionCallback=lambda: Datagroup(assetId, partitionName, datagroupType, name, subPath).delete(),
            objectName=datagroupName,
            assetId=assetId,
            partition=partitionName,
            objectType=datagroupType
        )



    def patch(self, request: Request, assetId: int, partitionName: str, datagroupType: str, datagroupName: str) -> Response:
        subPath, name = datagroupName.rsplit('~', 1) if '~' in datagroupName else ['', datagroupName]; subPath = subPath.replace('~', '/')

        return self.modify(
            request=request,
            actionCallback=lambda data: Datagroup(assetId, partitionName, datagroupType, name, subPath).modify(data),
            objectName=datagroupName,
            assetId=assetId,
            partition=partitionName,
            objectType=datagroupType,
            Serializer=Serializer
        )
