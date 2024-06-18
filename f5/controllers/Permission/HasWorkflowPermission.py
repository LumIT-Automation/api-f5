from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.Permission import Permission

from f5.controllers.CustomController import CustomController
from f5.helpers.Log import Log


class HasWorkflowPermissionController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int, partitionName: str, action: str) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="has_workflow_permission_get") or user["authDisabled"]:
                Log.actionLog("Check if use has workflow permission: "+action, user)

                if Permission.hasUserPermission(groups=user["groups"], action=action, assetId=assetId, partition=partitionName, isWorkflow=True):
                    httpStatus = status.HTTP_204_NO_CONTENT
                else:
                    httpStatus = status.HTTP_403_FORBIDDEN
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
