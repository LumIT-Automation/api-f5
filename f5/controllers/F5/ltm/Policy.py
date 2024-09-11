from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Policy import Policy

from f5.serializers.F5.ltm.Policy import F5PolicySerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update


class F5PolicyController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="policy", *args, **kwargs)


    def get(self, request: Request, assetId: int, partitionName: str, policyName: str) -> Response:
        subPath, name = policyName.rsplit('~', 1) if '~' in policyName else ['', policyName]; subPath = subPath.replace('~', '/')

        return self.getInfo(
            request=request,
            actionCallback=lambda: Policy(assetId, partitionName, name, subPath, loadRules=True).repr(),
            objectName=policyName,
            assetId=assetId,
            partitionName=partitionName
        )



    def delete(self, request: Request, assetId: int, partitionName: str, policyName: str) -> Response:
        subPath, name = policyName.rsplit('~', 1) if '~' in policyName else ['', policyName]; subPath = subPath.replace('~', '/')

        return self.remove(
            request=request,
            actionCallback=lambda: Policy(assetId, partitionName, name, subPath).delete(),
            objectName=policyName,
            assetId=assetId,
            partitionName=partitionName
        )



    def patch(self, request: Request, assetId: int, partitionName: str, policyName: str) -> Response:
        subPath, name = policyName.rsplit('~', 1) if '~' in policyName else ['', policyName]; subPath = subPath.replace('~', '/')

        return self.modify(
            request=request,
            actionCallback=lambda data: Policy(assetId, partitionName, name, subPath).modify(data),
            objectName=policyName,
            assetId=assetId,
            partitionName=partitionName,
            Serializer=Serializer
        )
