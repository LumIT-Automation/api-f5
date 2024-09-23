from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.CheckPermissionFacade import CheckPermissionFacade
from f5.models.F5.Usecases.VirtualServer import VirtualServerWorkflow

from f5.controllers.CustomController import CustomController

from f5.helpers.decorators.ReplicateVSDeletion import ReplicateVirtualServerDeletion
from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5WorkflowVirtualServerController(CustomController):
    @staticmethod
    @ReplicateVirtualServerDeletion
    def delete(request: Request, assetId: int, partitionName: str, virtualServerName: str) -> Response:
        subPath, name = virtualServerName.rsplit('~', 1) if '~' in virtualServerName else ['', virtualServerName]; subPath = subPath.replace('~', '/')
        replicaUuid = request.GET.get("__replicaUuid", "") # an uuid in order to correlate actions on logs.
        user = CustomController.loggedUser(request)
        workflowId = request.headers.get("workflowId", "")  # a correlation id.
        checkWorkflowPermission = request.headers.get("checkWorkflowPermission", "")

        try:
            if CheckPermissionFacade.hasUserPermission(groups=user["groups"], action="workflow_virtualServers_delete", isWorkflow=bool(workflowId), assetId=assetId, partition=partitionName) or user["authDisabled"]:
                if workflowId and checkWorkflowPermission:
                    httpStatus = status.HTTP_204_NO_CONTENT
                else:
                    Log.actionLog("Service deletion (workflow)", user)

                    lock = Lock(VirtualServerWorkflow.relatedF5Objects(), locals(), "any", workflowId=workflowId)
                    if lock.isUnlocked():
                        lock.lock()

                        VirtualServerWorkflow(assetId, partitionName, name, user, replicaUuid, subPath).delete()

                        httpStatus = status.HTTP_200_OK
                        if not workflowId:
                            lock.release()
                    else:
                        httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            if not workflowId:
                Lock(VirtualServerWorkflow.relatedF5Objects(), locals(), "any", workflowId=workflowId).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
