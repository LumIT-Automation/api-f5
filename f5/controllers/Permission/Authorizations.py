from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.Permission import Permission
from f5.controllers.CustomController import CustomController
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class AuthorizationsController(CustomController):
    @staticmethod
    # Enlist caller's permissions (depending on groups user belongs to).
    def get(request: Request) -> Response:
        etagCondition = {"responseEtag": ""}
        user = CustomController.loggedUser(request)

        try:
            if not user["authDisabled"]:
                Log.actionLog("Permissions' list", user)

                data = {
                    "data": {
                        "items": Permission.authorizationsList(user["groups"])
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
