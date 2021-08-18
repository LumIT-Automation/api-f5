from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Monitor import Monitor
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.Monitors import F5MonitorsSerializer as MonitorsSerializer
from f5.serializers.F5.Monitor import F5MonitorSerializer as MonitorSerializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5MonitorsController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int, partitionName: str, monitorType: str) -> Response:
        data = dict()
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="monitors_get", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Monitors list", user)

                lock = Lock("monitor", locals())
                if lock.isUnlocked():
                    lock.lock()

                    itemData = Monitor.list(assetId, partitionName, monitorType)
                    data["data"] = MonitorsSerializer(itemData).data["data"]
                    data["href"] = request.get_full_path()

                    # Check the response's ETag validity (against client request).
                    conditional = Conditional(request)
                    etagCondition = conditional.responseEtagFreshnessAgainstRequest(data["data"])
                    if etagCondition["state"] == "fresh":
                        data = None
                        httpStatus = status.HTTP_304_NOT_MODIFIED
                    else:
                        httpStatus = status.HTTP_200_OK

                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("monitor", locals()).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @staticmethod
    def post(request: Request, assetId: int, partitionName: str, monitorType: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="monitors_post", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Monitor addition", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = MonitorSerializer(data=request.data)
                if serializer.is_valid():
                    data = serializer.validated_data["data"]
                    data["partition"] = partitionName

                    lock = Lock("monitor", locals(), monitorType+data["name"])
                    if lock.isUnlocked():
                        lock.lock()

                        Monitor.add(assetId, monitorType, data)

                        httpStatus = status.HTTP_201_CREATED
                        lock.release()
                    else:
                        httpStatus = status.HTTP_423_LOCKED
                else:
                    httpStatus = status.HTTP_400_BAD_REQUEST
                    response = {
                        "F5": {
                            "error": str(serializer.errors)
                        }
                    }

                    Log.actionLog("User data incorrect: "+str(response), user)
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("monitor", locals(), locals()["monitorType"]+locals()["serializer"].data["data"]["name"]).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
