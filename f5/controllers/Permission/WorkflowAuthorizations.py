from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.WorkflowPermission import WorkflowPermission
from f5.controllers.CustomController import CustomController
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class WorkflowAuthorizationsController(CustomController):
    @staticmethod
    # Enlist caller's permissions (depending on groups user belongs to).
    def get(request: Request) -> Response:
        etagCondition = {"responseEtag": ""}
        user = CustomController.loggedUser(request)
        workflow = ""

        try:
            if not user["authDisabled"]:
                Log.actionLog("Workflow permissions' list", user)

                data = {
                    "data": {
                        "items": WorkflowPermission.workflowPermissionsList(user["groups"], workflow)
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
                httpStatus = status.HTTP_200_OK
        except Exception as e:
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })
