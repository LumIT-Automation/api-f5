from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.Permission import Permission
from f5.usecases.VirtualServer import VirtualServerWorkflow

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5WorkflowVirtualServerController(CustomController):
    @staticmethod
    def delete(request: Request, assetId: int, partitionName: str, virtualServerName: str) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="workflow_virtualServers_delete", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Service deletion (workflow)", user)

                lock = Lock(VirtualServerWorkflow.relatedF5Objects(), locals(), "any")
                if lock.isUnlocked():
                    lock.lock()

                    vsw = VirtualServerWorkflow(assetId, partitionName, virtualServerName, user)
                    vsw.delete()

                    httpStatus = status.HTTP_200_OK
                    lock.release()
                else:
                    httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock(VirtualServerWorkflow.relatedF5Objects(), locals(), "any").release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
