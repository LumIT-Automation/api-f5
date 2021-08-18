from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.VirtualServer import VirtualServer
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.VirtualServer import F5VirtualServerSerializer as Serializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5VirtualServerController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int, partitionName: str, virtualServerName: str) -> Response:
        data = dict()
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="virtualServer_get", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Virtual server information", user)

                lock = Lock("virtualServer", locals())
                if lock.isUnlocked():
                    lock.lock()

                    vs = VirtualServer(assetId, partitionName, virtualServerName)
                    itemData = vs.info()

                    data["data"] = Serializer(itemData).data["data"]
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
            Lock("virtualServer", locals()).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @staticmethod
    def delete(request: Request, assetId: int, partitionName: str, virtualServerName: str) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="virtualServer_delete", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Virtual server deletion", user)

                lock = Lock("virtualServer", locals(), virtualServerName)
                if lock.isUnlocked():
                    lock.lock()

                    vs = VirtualServer(assetId, partitionName, virtualServerName)
                    vs.delete()

                    httpStatus = status.HTTP_200_OK
                    lock.release()
                else:
                    httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("virtualServer", locals(), locals()["virtualServerName"]).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    @staticmethod
    def patch(request: Request, assetId: int, partitionName: str, virtualServerName: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="virtualServer_patch", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Virtual server modification", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = Serializer(data=request.data, partial=True)
                if serializer.is_valid():
                    data = serializer.validated_data["data"]
                    data["partition"] = partitionName

                    lock = Lock("virtualServer", locals(), virtualServerName)
                    if lock.isUnlocked():
                        lock.lock()

                        vs = VirtualServer(assetId, partitionName, virtualServerName)
                        vs.modify(data)

                        httpStatus = status.HTTP_200_OK
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
            Lock("virtualServer", locals(), locals()["virtualServerName"]).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
