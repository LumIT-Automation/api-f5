from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Pool import Pool
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.PoolMember import F5PoolMemberSerializer as Serializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5PoolMemberController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int, partitionName: str, poolName: str, poolMemberName: str) -> Response:
        data = dict()
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="poolMember_get", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Pool member information", user)

                lock = Lock("poolMember", locals())
                if lock.isUnlocked():
                    lock.lock()

                    pm = Pool(assetId, poolName, partitionName).member(poolMemberName)
                    itemData = pm.info()

                    data["data"] = Serializer(itemData).data
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
            Lock("poolMember", locals()).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @staticmethod
    def delete(request: Request, assetId: int, partitionName: str, poolName: str, poolMemberName: str) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="poolMember_delete", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Pool members deletion", user)

                lock = Lock("poolMember", locals(), poolMemberName)
                if lock.isUnlocked():
                    lock.lock()

                    pm = Pool(assetId, poolName, partitionName).member(poolMemberName)
                    pm.delete()

                    httpStatus = status.HTTP_200_OK
                    lock.release()
                else:
                    httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("poolMember", locals(), locals()["poolMemberName"]).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    @staticmethod
    def patch(request: Request, assetId: int, partitionName: str, poolName: str, poolMemberName: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="poolMember_patch", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Pool members modify", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = Serializer(data=request.data["data"], partial=True)
                if serializer.is_valid():
                    data = serializer.validated_data

                    lock = Lock("poolMember", locals(), poolMemberName)
                    if lock.isUnlocked():
                        lock.lock()

                        pm = Pool(assetId, poolName, partitionName).member(poolMemberName)
                        pm.modify(data)

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
            Lock("poolMember", locals(), locals()["poolMemberName"]).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
