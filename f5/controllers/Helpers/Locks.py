from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.helpers.Lock import Lock
from f5.models.Permission.CheckPermissionFacade import CheckPermissionFacade

from f5.controllers.CustomController import CustomController

from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5LocksController(CustomController):
    @staticmethod
    def get(request: Request, workflowId: str) -> Response:
        etagCondition = { "responseEtag": "" }
        user = CustomController.loggedUser(request)

        try:
            if CheckPermissionFacade.hasUserPermission(groups=user["groups"], action="locks_get") or user["authDisabled"]:
                Log.actionLog("Locks list", user)
                data = {
                    "data": {
                        "items": Lock.listWorkflowLocks(workflowId=workflowId)
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
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



class F5LocksUnlockController(CustomController):
    @staticmethod
    def delete(request: Request) -> Response:
        user = CustomController.loggedUser(request)
        workflowId = request.headers.get("workflowId", "") # a correlation id.
        checkWorkflowPermission = request.headers.get("checkWorkflowPermission", "")
        httpStatus = status.HTTP_500_INTERNAL_SERVER_ERROR

        try:
            if not workflowId:
                httpStatus = status.HTTP_400_BAD_REQUEST
            else:
                if CheckPermissionFacade.hasUserPermission(groups=user["groups"], action="locks_delete", isWorkflow=bool(workflowId)) or user["authDisabled"]:
                    if workflowId and checkWorkflowPermission:
                        httpStatus = status.HTTP_204_NO_CONTENT
                    elif workflowId:
                        Log.actionLog("Unlock workflow objects: "+workflowId, user)
                        Lock.releaseWorkflow(workflowId)
                        httpStatus = status.HTTP_200_OK
                else:
                    httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })

