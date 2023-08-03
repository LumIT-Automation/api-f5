from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.auth.Partition import Partition
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.Partitions import F5PartitionsSerializer as Serializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5PartitionsController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int) -> Response:
        data = dict()
        allowedData = {"items": list()}
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="partitions_get", assetId=assetId) or user["authDisabled"]:
                Log.actionLog("Partitions list", user)

                lock = Lock("partition", locals())
                if lock.isUnlocked():
                    lock.lock()

                    # Filter partitions' list basing on actual permissions.
                    for p in Partition.list(assetId):
                        if Permission.hasUserPermission(groups=user["groups"], action="partitions_get", assetId=assetId, partition=str(p["fullPath"])) or user["authDisabled"]:
                            allowedData["items"].append(p)

                    data["data"] = Serializer(allowedData).data
                    data["href"] = request.get_full_path()

                    httpStatus = status.HTTP_200_OK
                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("partition", locals()).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
