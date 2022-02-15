from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Certificate import Certificate
from f5.models.F5.Key import Key
from f5.models.Permission.Permission import Permission

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5CertificateController(CustomController):
    @staticmethod
    def delete(request: Request, assetId: int, partitionName: str, resourceName: str) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="certificate_delete", assetId=assetId) or user["authDisabled"]:
                Log.actionLog("Certificate or key deletion", user)

                if "certificate" in request.get_full_path():
                    lock = Lock("certificate", locals(), resourceName)
                    if lock.isUnlocked():
                        lock.lock()

                        c = Certificate(assetId, partitionName, resourceName)
                        c.delete()

                        httpStatus = status.HTTP_200_OK
                        lock.release()
                    else:
                        httpStatus = status.HTTP_423_LOCKED

                elif "key" in request.get_full_path():
                    lock = Lock("key", locals(), resourceName)
                    if lock.isUnlocked():
                        lock.lock()

                        k = Key(assetId, partitionName, resourceName)
                        k.delete()

                        httpStatus = status.HTTP_200_OK
                        lock.release()
                    else:
                        httpStatus = status.HTTP_423_LOCKED
                else:
                    httpStatus = status.HTTP_400_BAD_REQUEST
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            # (Lock released after timeout).
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
