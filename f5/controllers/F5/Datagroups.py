import threading

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Datagroup import Datagroup
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.Datagroups import F5DatagroupsSerializer as DatagroupsSerializer
from f5.serializers.F5.Datagroup import F5DatagroupSerializer as DatagroupSerializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5DatagroupsController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int, partitionName: str, datagroupType: str = "") -> Response:
        data = {"data": dict()}
        itemData = dict()
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="monitors_get", assetId=assetId, partitionName=partitionName) or user["authDisabled"]: # @todo: datagroups_get
                Log.actionLog("Datagroups list", user)

                lock = Lock("datagroup", locals())
                if lock.isUnlocked():
                    lock.lock()

                    if datagroupType:
                        if datagroupType != "ANY":
                            # Datagroups list of that type.
                            itemData["items"] = Datagroup.list(assetId, partitionName, datagroupType)
                            data["data"] = DatagroupsSerializer(itemData).data
                        else:
                            # All datagroups, of any type.
                            datagroupType = Datagroup.types(assetId, partitionName)

                            # The threading way.
                            # This requires a consistent throttle on remote appliance.
                            def datagroupsListOfType(dgType):
                                itemData["items"] = Datagroup.list(assetId, partitionName, dgType)
                                data["data"][dgType] = DatagroupsSerializer(itemData).data

                            workers = [threading.Thread(target=datagroupsListOfType, args=(m,)) for m in datagroupType]
                            for w in workers:
                                w.start()
                            for w in workers:
                                w.join()
                    else:
                        # Datagroups types list.
                        # No need for a serializer: just a list of strings.
                        data["data"]["items"] = Datagroup.types(assetId, partitionName)

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
            Lock("datagroup", locals()).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @staticmethod
    def post(request: Request, assetId: int, partitionName: str, datagroupType: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="monitors_post", assetId=assetId, partitionName=partitionName) or user["authDisabled"]: # @todo: datagroups_post.
                Log.actionLog("Datagroup addition", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = DatagroupSerializer(data=request.data["data"])
                if serializer.is_valid():
                    data = serializer.validated_data
                    data["partition"] = partitionName

                    lock = Lock("datagroup", locals(), datagroupType+data["name"])
                    if lock.isUnlocked():
                        lock.lock()

                        Datagroup.add(assetId, datagroupType, data)

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
                Lock("datagroup", locals(), locals()["datagroupType"]+locals()["serializer"].data["name"]).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
