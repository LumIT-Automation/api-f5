from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Pool import Pool
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.Pool import F5PoolSerializer as Serializer

from f5.controllers.CustomController import CustomController

from f5.helpers.AssetDr import AssetDr
from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5PoolController(CustomController):
    @staticmethod
    @AssetDr
    def delete(request: Request, assetId: int, partitionName: str, poolName: str) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="pool_delete", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Pool deletion", user)

                lock = Lock("pool", locals(), poolName)
                if lock.isUnlocked():
                    lock.lock()

                    Pool(assetId, partitionName, poolName).delete()

                    httpStatus = status.HTTP_200_OK
                    lock.release()
                else:
                    httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("pool", locals(), poolName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    @staticmethod
    @AssetDr
    def patch(request: Request, assetId: int, partitionName: str, poolName: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="pool_patch", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Pool modification", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = Serializer(data=request.data["data"], partial=True)
                if serializer.is_valid():
                    data = serializer.validated_data

                    lock = Lock("pool", locals(), poolName)
                    if lock.isUnlocked():
                        lock.lock()

                        Pool(assetId, partitionName, poolName).modify(data)

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
            Lock("pool", locals(), poolName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
