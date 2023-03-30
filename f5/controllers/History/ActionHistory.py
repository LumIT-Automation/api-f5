from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.History.ActionHistory import ActionHistory
from f5.models.Permission.Permission import Permission

from f5.serializers.History.ActionHistory import ActionHistorySerializer as Serializer

from f5.controllers.CustomController import CustomController
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class ActionHistoryLogsController(CustomController):
    @staticmethod
    def get(request: Request) -> Response:
        allUsersHistory = False
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="historyDrComplete_get") or user["authDisabled"]:
                allUsersHistory = True

            Log.actionLog("Action History", user)

            data = {
                "data": {
                    "items": CustomController.validate(
                        ActionHistory.dataList(user["username"], allUsersHistory),
                        Serializer,
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
        except Exception as e:
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })
