from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Profile import Profile

from f5.serializers.F5.ltm.Profile import F5ProfileSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update


class F5ProfileController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="monitor", *args, **kwargs)


    def get(self, request: Request, assetId: int, partitionName: str, profileType: str, profileName: str) -> Response:
        subPath, name = profileName.rsplit('~', 1) if '~' in profileName else ['', profileName]; subPath = subPath.replace('~', '/')

        return self.getInfo(
            request=request,
            actionCallback=lambda: Profile(assetId, partitionName, profileType, name, subPath).repr(),
            objectName=profileName,
            assetId=assetId,
            partitionName=partitionName,
            objectType=profileType
        )



    def delete(self, request: Request, assetId: int, partitionName: str, profileType: str, profileName: str) -> Response:
        subPath, name = profileName.rsplit('~', 1) if '~' in profileName else ['', profileName]; subPath = subPath.replace('~', '/')

        return self.remove(
            request=request,
            actionCallback=lambda: Profile(assetId, partitionName, profileType, name, subPath).delete(),
            objectName=profileName,
            assetId=assetId,
            partitionName=partitionName,
            objectType=profileType
        )



    def patch(self, request: Request, assetId: int, partitionName: str, profileType: str, profileName: str) -> Response:
        subPath, name = profileName.rsplit('~', 1) if '~' in profileName else ['', profileName]; subPath = subPath.replace('~', '/')

        return self.modify(
            request=request,
            actionCallback=lambda data: Profile(assetId, partitionName, profileType, name, subPath).modify(data),
            objectName=profileName,
            assetId=assetId,
            partitionName=partitionName,
            objectType=profileType,
            Serializer=Serializer
        )
