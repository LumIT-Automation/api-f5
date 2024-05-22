from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.Permission import Permission
from f5.models.F5.Usecases.CertificateUpdate import CertificateUpdateWorkflow

from f5.serializers.F5.Usecases.CertificateUpdate import F5CertificateUpdateSerializer as WorkflowCertificateSerializer

from f5.controllers.CustomController import CustomController

from f5.helpers.decorators.ReplicateVSCreation import ReplicateVirtualServerCreation
from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5WorkflowCertificateUpdateController(CustomController):
    @staticmethod
    @ReplicateVirtualServerCreation
    def put(request: Request, assetId: int, partitionName: str, profileName: str) -> Response:
        response = None
        replicaUuid = request.GET.get("__replicaUuid", "") # an uuid in order to correlate actions on logs.

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="service_certificate_put", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Certificate update service", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = WorkflowCertificateSerializer(data=request.data)
                if serializer.is_valid():
                    data = serializer.validated_data["data"]

                    lock = Lock("profile", locals(), "client-ssl"+profileName)
                    if lock.isUnlocked():
                        lock.lock()

                        CertificateUpdateWorkflow(assetId, partitionName, profileName, user, replicaUuid).updateCert(data)

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
            Lock("profile", locals(), "client-ssl"+profileName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
