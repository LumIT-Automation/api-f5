from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Certificate import Certificate
from f5.models.F5.Key import Key
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.Certificate import F5CertificateSerializer as CertificateSerializer
from f5.serializers.F5.Certificates import F5CertificatesSerializer as CertificatesSerializer
from f5.serializers.F5.Key import F5KeySerializer as KeySerializer
from f5.serializers.F5.Keys import F5KeysSerializer as KeysSerializer

from f5.controllers.CustomController import CustomController

from f5.helpers.AssetDr import AssetDr
from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5CertificatesController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int, partitionName: str) -> Response:
        data = dict()
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="certificates_get", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("List certificate or key", user)

                if "certificates" in request.get_full_path():
                    lock = Lock("certificate", locals())
                    if lock.isUnlocked():
                        lock.lock()

                        data = {
                            "data": {
                                "items": CustomController.validate(
                                    Certificate.list(assetId, partitionName),
                                    CertificatesSerializer,
                                    "list"
                                )
                            },
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

                elif "keys" in request.get_full_path():
                    lock = Lock("key", locals())
                    if lock.isUnlocked():
                        lock.lock()

                        data = {
                            "data": {
                                "items": CustomController.validate(
                                    Key.list(assetId, partitionName),
                                    KeysSerializer,
                                    "list"
                                )
                            },
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
                    httpStatus = status.HTTP_400_BAD_REQUEST
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("certificate", locals()).release()
            Lock("key", locals()).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @staticmethod
    def post(request: Request, assetId: int, partitionName: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="certificates_post", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Upload certificate or key", user)
                Log.actionLog("User data: "+str(request.data), user)

                if "certificate" in request.data:
                    serializer = CertificateSerializer(data=request.data)
                    if serializer.is_valid():
                        data = serializer.validated_data["certificate"]

                        lock = Lock("certificate", locals(), data["name"])
                        if lock.isUnlocked():
                            lock.lock()

                            Certificate.install(assetId, partitionName, data)

                            lock.release()
                            httpStatus = status.HTTP_201_CREATED
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

                elif "key" in request.data:
                    serializer = KeySerializer(data=request.data)
                    if serializer.is_valid():
                        data = serializer.validated_data["key"]

                        lock = Lock("key", locals(), data["name"])
                        if lock.isUnlocked():
                            lock.lock()

                            Key.install(assetId, partitionName, data)

                            lock.release()
                            httpStatus = status.HTTP_201_CREATED
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
            if "serializer" in locals():
                if "certificate" in locals()["serializer"].data:
                    Lock("certificate", locals(), locals()["serializer"].data["certificate"]["name"]).release()

                if "key" in locals()["serializer"].data:
                    Lock("key", locals(), locals()["serializer"].data["key"]["name"]).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
