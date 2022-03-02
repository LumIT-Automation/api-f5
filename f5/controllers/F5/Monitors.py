#import asyncio
#from asgiref.sync import sync_to_async
import threading

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
    def get(request: Request, assetId: int, partitionName: str, monitorType: str = "") -> Response:
        data = {"data": dict()}
        itemData = dict()
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="monitors_get", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Monitors list", user)

                lock = Lock("monitor", locals())
                if lock.isUnlocked():
                    lock.lock()

                    if monitorType:
                        if monitorType != "ANY":
                            # Monitors' list of that type.
                            # F5 treats monitor type as a sub-object instead of a property. Odd.
                            itemData["items"] = Monitor.list(assetId, partitionName, monitorType)
                            data["data"] = MonitorsSerializer(itemData).data
                        else:
                            monitorTypes = Monitor.types(assetId, partitionName)

                            # Event driven calls (no: still serialized).
                            # @sync_to_async
                            # def monitorsListOfType(mType):
                            #     r = dict()
                            #     r[mType] = MonitorsSerializer(
                            #         Monitor.list(assetId, partitionName, mType)
                            #     ).data
                            #
                            #     return r
                            #
                            # loop = asyncio.get_event_loop()
                            # coroutines = [monitorsListOfType(m) for m in monitorTypes]
                            # data["data"] = loop.run_until_complete(asyncio.gather(*coroutines))
                            # loop.close()

                            # The threading way.
                            # This requires a consistent throttle on remote appliance.
                            def monitorsListOfType(mType):
                                itemData["items"] = Monitor.list(assetId, partitionName, mType)
                                data["data"][mType] = MonitorsSerializer(itemData).data

                            workers = [threading.Thread(target=monitorsListOfType, args=(m,)) for m in monitorTypes]
                            for w in workers:
                                w.start()
                            for w in workers:
                                w.join()
                    else:
                        # Monitors' types list.
                        # No need for a serializer: just a list of strings.
                        data["data"]["items"] = Monitor.types(assetId, partitionName)

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

                serializer = MonitorSerializer(data=request.data["data"])
                if serializer.is_valid():
                    data = serializer.validated_data
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
            if "serializer" in locals():
                Lock("monitor", locals(), locals()["monitorType"]+locals()["serializer"].data["name"]).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
