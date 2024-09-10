import threading

from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Monitor import Monitor

from f5.serializers.F5.ltm.Monitors import F5MonitorsSerializer as MonitorsSerializer
from f5.serializers.F5.ltm.Monitor import F5MonitorSerializer as MonitorSerializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList
from f5.controllers.CustomControllerPost import CustomControllerF5Create



class F5MonitorsController(CustomControllerF5GetList, CustomControllerF5Create):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="monitor", *args, **kwargs)



    def get(self, request: Request, assetId: int, partitionName: str, monitorType: str = "") -> Response:
        def actionCallback():
            data = {"data": dict()}
            itemData = dict()

            if monitorType:
                if monitorType != "ANY":
                    # Monitors' list of that type.
                    # F5 treats monitor type as a sub-object instead of a property. Odd.
                    itemData["items"] = Monitor.dataList(assetId, partitionName, monitorType)
                    data["data"] = MonitorsSerializer(itemData).data
                else:
                    monitorTypes = Monitor.types(assetId, partitionName)

                    # The threading way.
                    # This requires a consistent throttle on remote appliance.
                    def monitorsListOfType(mType):
                        itemData["items"] = Monitor.dataList(assetId, partitionName, mType)
                        data["data"][mType] = MonitorsSerializer(itemData).data

                    workers = [threading.Thread(target=monitorsListOfType, args=(m,)) for m in monitorTypes]
                    for w in workers:
                        w.start()
                    for w in workers:
                        w.join()
            else:
                # Monitors' types list.
                data["data"]["items"] = Monitor.types(assetId, partitionName)

            data["href"] = request.get_full_path()
            return data


        return self.getList(
            request=request,
            actionCallback=actionCallback,
            assetId=assetId,
            partition=partitionName,
            objectType=monitorType,
            customCallback=True
        )



    def post(self, request: Request, assetId: int, partitionName: str, monitorType: str) -> Response:
        def dataFix(data: dict):
            data["partition"] = partitionName
            return data


        return self.create(
            request=request,
            actionCallback=lambda data: Monitor.add(assetId, monitorType, data),
            assetId=assetId,
            partition=partitionName,
            objectType=monitorType,
            Serializer=MonitorSerializer,
            lockItemField="name",
            dataFix=dataFix
        )
