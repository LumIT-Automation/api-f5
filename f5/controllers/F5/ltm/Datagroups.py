import threading

from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Datagroup import Datagroup

from f5.serializers.F5.ltm.Datagroups import F5DatagroupsSerializer as DatagroupsSerializer
from f5.serializers.F5.ltm.Datagroup import F5DatagroupSerializer as DatagroupSerializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList
from f5.controllers.CustomControllerPost import CustomControllerF5Create


class F5DatagroupsController(CustomControllerF5GetList, CustomControllerF5Create):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="datagroup", *args, **kwargs)

    def get(self, request: Request, assetId: int, partitionName: str, datagroupType: str = "") -> Response:
        def actionCallback():
            data = {"data": dict()}
            itemData = dict()

            if datagroupType:
                if datagroupType != "ANY":
                    # Datagroups list of that type.e.
                    itemData["items"] = Datagroup.dataList(assetId, partitionName, datagroupType)
                    data["data"] = DatagroupsSerializer(itemData).data
                else:
                    datagroupTypes = Datagroup.types(assetId, partitionName)

                    # The threading way.
                    # This requires a consistent throttle on remote appliance.
                    def datagroupsListOfType(dgType):
                        itemData["items"] = Datagroup.dataList(assetId, partitionName, dgType)
                        data["data"][dgType] = DatagroupsSerializer(itemData).data

                    workers = [threading.Thread(target=datagroupsListOfType, args=(m,)) for m in datagroupTypes]
                    for w in workers:
                        w.start()
                    for w in workers:
                        w.join()
            else:
                # Datagroups types list.
                # No need for a serializer: just a list of strings.
                data["data"]["items"] = Datagroup.types(assetId, partitionName)

            data["href"] = request.get_full_path()
            return data


        return self.getList(
            request=request,
            actionCallback=actionCallback,
            assetId=assetId,
            partition=partitionName,
            objectType=datagroupType,
            customCallback=True
        )



    def post(self, request: Request, assetId: int, partitionName: str, datagroupType: str) -> Response:
        def dataFix(data: dict):
            data["partition"] = partitionName
            return data


        return self.create(
            request=request,
            actionCallback=lambda data: Datagroup.add(assetId, datagroupType, data),
            assetId=assetId,
            partition=partitionName,
            objectType=datagroupType,
            Serializer=DatagroupSerializer,
            lockItemDataKey="name",
            dataFix=dataFix
        )
