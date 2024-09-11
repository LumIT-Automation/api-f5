from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Pool import Pool

from f5.serializers.F5.ltm.PoolMembers import F5PoolMembersSerializer as PoolMembersSerializer
from f5.serializers.F5.ltm.PoolMember import F5PoolMemberSerializer as PoolMemberSerializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList
from f5.controllers.CustomControllerPost import CustomControllerF5Create



class F5PoolMembersController(CustomControllerF5GetList, CustomControllerF5Create):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="poolMember", *args, **kwargs)



    def get(self, request: Request, assetId: int, partitionName: str, poolName: str) -> Response:
        subPath, name = poolName.rsplit('~', 1) if '~' in poolName else ['', poolName]; subPath = subPath.replace('~', '/')

        return self.getList(
            request=request,
            actionCallback=lambda: Pool(assetId, partitionName, name, subPath).getMembersData(),
            assetId=assetId,
            partition=partitionName,
            Serializer=PoolMembersSerializer,
            parentSubject="pool",
            parentName=poolName
        )



    def post(self, request: Request, assetId: int, partitionName: str, poolName: str) -> Response:
        subPath, name = poolName.rsplit('~', 1) if '~' in poolName else ['', poolName]; subPath = subPath.replace('~', '/')

        def dataFix(data: dict):
            if "state" in data:
                data["State"] = data["state"]  # curious F5 field's name.
                del (data["state"])

            return data


        return self.create(
            request=request,
            actionCallback=lambda data: Pool(assetId, partitionName, name, subPath).addMember(data),
            assetId=assetId,
            partition=partitionName,
            Serializer=PoolMemberSerializer,
            lockItemDataKey="name",
            dataFix=dataFix,
            parentSubject="pool",
            parentName=poolName
        )
