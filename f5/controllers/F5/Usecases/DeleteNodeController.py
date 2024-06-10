from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.Permission import Permission
from f5.models.F5.Usecases.DeleteNode import DeleteNodeWorkflow

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5WorkflowDeleteNodeController(CustomController):
    @staticmethod
    def delete(request: Request, assetId: int, partitionName: str, nodeName: str) -> Response:
        subPath, name = nodeName.rsplit('~', 1) if '~' in nodeName else ['', nodeName]; subPath = subPath.replace('~', '/')
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="workflow_node_delete", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Node deletion (workflow)", user)

                lock = Lock("node", locals(), nodeName)
                lock = Lock("pool", locals(), "any")
                if lock.isUnlocked():
                    lock.lock()

                    DeleteNodeWorkflow(assetId, partitionName, name, user, subPath).delete()

                    httpStatus = status.HTTP_200_OK
                    lock.release()
                else:
                    httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("pool", locals(), "any").release()
            Lock("node", locals(), nodeName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
