from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Certificate import Certificate
from f5.models.F5.Key import Key
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.Certificate import F5CertificateSerializer as CertificateSerializer
from f5.serializers.F5.Key import F5KeySerializer as KeySerializer

from f5.controllers.CustomController import CustomController

from f5.helpers.AssetDr import AssetDr
from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5CertificateController(CustomController):
    @staticmethod
    @AssetDr
    def delete(request: Request, assetId: int, partitionName: str, resourceName: str) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="certificate_delete", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Certificate or key deletion", user)

                if "certificate" in request.get_full_path():
                    lock = Lock("certificate", locals(), resourceName)
                    if lock.isUnlocked():
                        lock.lock()

                        Certificate(assetId, partitionName, resourceName).delete()

                        httpStatus = status.HTTP_200_OK
                        lock.release()
                    else:
                        httpStatus = status.HTTP_423_LOCKED

                elif "key" in request.get_full_path():
                    lock = Lock("key", locals(), resourceName)
                    if lock.isUnlocked():
                        lock.lock()

                        Key(assetId, partitionName, resourceName).delete()

                        httpStatus = status.HTTP_200_OK
                        lock.release()
                    else:
                        httpStatus = status.HTTP_423_LOCKED
                else:
                    httpStatus = status.HTTP_400_BAD_REQUEST
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("certificate", locals(), resourceName).release()
            Lock("key", locals(), resourceName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    @staticmethod
    @AssetDr
    def patch(request: Request, assetId: int, partitionName: str, resourceName: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="certificates_post", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Certificate or key modification", user)
                Log.actionLog("User data: "+str(request.data), user)

                if "certificate" in request.get_full_path():
                    serializer = CertificateSerializer(data=request.data, partial=True)
                    if serializer.is_valid():
                        data = serializer.validated_data["certificate"]

                        lock = Lock("certificate", locals(), resourceName)
                        if lock.isUnlocked():
                            lock.lock()

                            Certificate(assetId, partitionName, resourceName).update(data)

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
                elif "key" in request.get_full_path():
                    serializer = KeySerializer(data=request.data, partial=True)
                    if serializer.is_valid():
                        data = serializer.validated_data["key"]

                        lock = Lock("key", locals(), resourceName)
                        if lock.isUnlocked():
                            lock.lock()

                            Key(assetId, partitionName, resourceName).update(data)

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

                        Log.actionLog("User data incorrect: " + str(response), user)
                else:
                    httpStatus = status.HTTP_400_BAD_REQUEST
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("certificate", locals(), resourceName).release()
            Lock("key", locals(), resourceName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
