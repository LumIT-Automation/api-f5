from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.VirtualServer import VirtualServer

from f5.serializers.F5.ltm.VirtualServers import F5VirtualServersSerializer as VirtualServersSerializer
from f5.serializers.F5.ltm.VirtualServer import F5VirtualServerSerializer as VirtualServerSerializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList
from f5.controllers.CustomControllerPost import CustomControllerF5Create
from f5.helpers.Exception import CustomException



class F5VirtualServersController(CustomControllerF5GetList, CustomControllerF5Create):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="virtualserver", *args, **kwargs)



    def get(self, request: Request, assetId: int, partitionName: str) -> Response:
        loadPolicies= False
        loadProfiles = False

        try:
            if "related" in request.GET:
                rList = request.GET.get("related")
                if "policies" in rList:
                    loadPolicies = True
                if "profiles" in rList:
                    loadProfiles = True
        except Exception as e:
            raise CustomException(status=400, payload={"F5": "Bad url parameter."})

        return self.getList(
            request=request,
            actionCallback=lambda: [r.repr() for r in VirtualServer.list(assetId, partitionName, loadPolicies=loadPolicies, loadProfiles=loadProfiles)],
            assetId=assetId,
            partition=partitionName,
            Serializer=VirtualServersSerializer
        )



    def post(self, request: Request, assetId: int, partitionName: str) -> Response:
        def dataFix(data: dict):
            data["partition"] = partitionName
            return data


        return self.create(
            request=request,
            actionCallback=lambda data: VirtualServer.add(assetId, data),
            assetId=assetId,
            partition=partitionName,
            Serializer=VirtualServerSerializer,
            lockItemField="name",
            dataFix=dataFix,
        )
