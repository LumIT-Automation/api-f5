from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Policy import Policy

from f5.serializers.F5.ltm.Policies import F5PoliciesSerializer as PoliciesSerializer
from f5.serializers.F5.ltm.Policy import F5PolicySerializer as PolicySerializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList
from f5.controllers.CustomControllerPost import CustomControllerF5Create


class F5PoliciesController(CustomControllerF5GetList, CustomControllerF5Create):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="policy", *args, **kwargs)



    def get(self, request: Request, assetId: int, partitionName: str) -> Response:

        return self.getList(
            request=request,
            actionCallback=lambda: [r.repr() for r in Policy.list(assetId, partitionName, loadRules=True)],
            assetId=assetId,
            partition=partitionName,
            Serializer=PoliciesSerializer
        )



    def post(self, request: Request, assetId: int, partitionName: str) -> Response:
        def dataFix(data: dict):
            data["partition"] = partitionName
            return data


        return self.create(
            request=request,
            actionCallback=lambda data: Policy.add(assetId, data),
            assetId=assetId,
            partition=partitionName,
            Serializer=PolicySerializer,
            lockItemField="name",
            dataFix=dataFix,
        )
