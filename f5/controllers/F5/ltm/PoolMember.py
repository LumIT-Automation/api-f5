from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Pool import Pool

from f5.serializers.F5.ltm.PoolMember import F5PoolMemberSerializer as Serializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update


class F5PoolMemberController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="poolMember", *args, **kwargs)


    def get(self, request: Request, assetId: int, partitionName: str, poolName: str, poolMemberName: str) -> Response:
        poolSubPath, pool = poolName.rsplit('~', 1) if '~' in poolName else ['', poolName]; poolSubPath = poolSubPath.replace('~', '/')
        memberSubPath, poolMember = poolMemberName.rsplit('~', 1) if '~' in poolMemberName else ['', poolMemberName]; memberSubPath = memberSubPath.replace('~', '/')

        return self.getInfo(
            request=request,
            actionCallback=lambda: Pool(assetId, pool, partitionName, poolSubPath).getMember(poolMember, memberSubPath).info(),
            objectName=poolMemberName,
            assetId=assetId,
            partition=partitionName,
            parentSubject="pool",
            parentName=poolName
        )



    def delete(self, request: Request, assetId: int, partitionName: str, poolName: str, poolMemberName: str) -> Response:
        poolSubPath, pool = poolName.rsplit('~', 1) if '~' in poolName else ['', poolName]; poolSubPath = poolSubPath.replace('~', '/')
        memberSubPath, poolMember = poolMemberName.rsplit('~', 1) if '~' in poolMemberName else ['', poolMemberName]; memberSubPath = memberSubPath.replace('~', '/')

        return self.remove(
            request=request,
            actionCallback=lambda: Pool(assetId, pool, partitionName, poolSubPath).getMember(poolMember, memberSubPath).delete(),
            objectName=poolMemberName,
            assetId=assetId,
            partition=partitionName,
            parentSubject="pool",
            parentName=poolName
        )



    def patch(self, request: Request, assetId: int, partitionName: str, poolName: str, poolMemberName: str) -> Response:
        poolSubPath, pool = poolName.rsplit('~', 1) if '~' in poolName else ['', poolName]; poolSubPath = poolSubPath.replace('~', '/')
        memberSubPath, poolMember = poolMemberName.rsplit('~', 1) if '~' in poolMemberName else ['', poolMemberName]; memberSubPath = memberSubPath.replace('~', '/')

        return self.modify(
            request=request,
            actionCallback=lambda data: Pool(assetId, pool, partitionName, poolSubPath).getMember(poolMember, memberSubPath).modify(data),
            objectName=poolMemberName,
            assetId=assetId,
            partition=partitionName,
            Serializer=Serializer,
            parentSubject="pool",
            parentName=poolName
        )
