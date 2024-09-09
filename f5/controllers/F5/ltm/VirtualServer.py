from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.VirtualServer import VirtualServer

from f5.serializers.F5.ltm.VirtualServer import F5VirtualServerSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update
from f5.helpers.Exception import CustomException

class F5VirtualServerController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="virtualServer", *args, **kwargs)


    def get(self, request: Request, assetId: int, partitionName: str, virtualServerName: str) -> Response:
        subPath, name = virtualServerName.rsplit('~', 1) if '~' in virtualServerName else ['', virtualServerName]; subPath = subPath.replace('~', '/')
        loadPolicies= False
        loadProfiles = False
        profileTypeFilter = []

        try:
            if "related" in request.GET:
                rList = request.GET.get("related")
                if "policies" in rList:
                    loadPolicies = True
                if "profiles" in rList:
                    loadProfiles = True
            if "profileType" in request.GET:
                profileTypeFilter = request.GET.get("profileType").split(',')
        except Exception as e:
            raise CustomException(status=400, payload={"F5": "Bad url parameter."})

        return self.getInfo(
            request=request,
            actionCallback=lambda: VirtualServer(assetId, partitionName, name, subPath, loadPolicies=loadPolicies, loadProfiles=loadProfiles, profileTypeFilter=profileTypeFilter).repr(),
            objectName=virtualServerName,
            assetId=assetId,
            partition=partitionName
        )



    def delete(self, request: Request, assetId: int, partitionName: str, virtualServerName: str) -> Response:
        subPath, name = virtualServerName.rsplit('~', 1) if '~' in virtualServerName else ['', virtualServerName]; subPath = subPath.replace('~', '/')

        return self.remove(
            request=request,
            actionCallback=lambda: VirtualServer(assetId, partitionName, name, subPath).delete(),
            objectName=virtualServerName,
            assetId=assetId,
            partition=partitionName
        )



    def patch(self, request: Request, assetId: int, partitionName: str, virtualServerName: str) -> Response:
        subPath, name = virtualServerName.rsplit('~', 1) if '~' in virtualServerName else ['', virtualServerName]; subPath = subPath.replace('~', '/')

        return self.modify(
            request=request,
            actionCallback=lambda data: VirtualServer(assetId, partitionName, name, subPath).modify(data),
            objectName=virtualServerName,
            assetId=assetId,
            partition=partitionName,
            Serializer=Serializer
        )
