from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.CheckPermissionFacade import CheckPermissionFacade
from f5.models.F5.Usecases.DeleteNode import DeleteNodeWorkflow

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Locker
from f5.helpers.Log import Log


class F5WorkflowDeleteNodeController(CustomController):
    @staticmethod
    def delete(request: Request, assetId: int, partitionName: str, nodeName: str) -> Response:
        subPath, name = nodeName.rsplit('~', 1) if '~' in nodeName else ['', nodeName]; subPath = subPath.replace('~', '/')
        user = CustomController.loggedUser(request)
        workflowId = request.headers.get("workflowId", "")  # a correlation id.
        checkWorkflowPermission = request.headers.get("checkWorkflowPermission", "")

        try:
            if CheckPermissionFacade.hasUserPermission(groups=user["groups"], action="workflow_node_delete", isWorkflow=bool(workflowId), assetId=assetId, partition=partitionName) or user["authDisabled"]:
                if workflowId and checkWorkflowPermission:
                    httpStatus = status.HTTP_204_NO_CONTENT
                else:
                    Log.actionLog("Node deletion (workflow)", user)

                    locker = Locker("node", locals(), nodeName, workflowId, "pool", "any")
                    if locker.isUnlocked():
                        locker.lock()

                        DeleteNodeWorkflow(assetId, partitionName, name, user, subPath).delete()

                        httpStatus = status.HTTP_200_OK
                        if not workflowId:
                            locker.release()
                    else:
                        httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            if not workflowId:
                Locker(objectClass="node", o=locals(), item=nodeName, parentObjectClass="pool", parentItem="any").release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
