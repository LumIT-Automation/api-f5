from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.sys.Folder import Folder
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.sys.Folders import F5FolderSerializer as Serializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5FolderController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int, partitionName: str, folderName: str) -> Response:
        data = dict()
        etagCondition = {"responseEtag": ""}

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="folder_get", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Folder information", user)

                lock = Lock("folder", locals(), folderName)
                if lock.isUnlocked():
                    lock.lock()

                    data = {
                        "data": CustomController.validate(
                            Folder(assetId, partitionName, folderName).info(),
                            Serializer,
                            "value"
                        ),
                        "href": request.get_full_path()
                    }

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
            Lock("folder", locals(), folderName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @staticmethod
    def delete(request: Request, assetId: int, partitionName: str, folderName: str) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="folder_delete", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Folder deletion", user)

                lock = Lock("folder", locals(), folderName)
                if lock.isUnlocked():
                    lock.lock()

                    Folder(assetId, partitionName, folderName).delete()

                    httpStatus = status.HTTP_200_OK
                    lock.release()
                else:
                    httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("folder", locals(), folderName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
