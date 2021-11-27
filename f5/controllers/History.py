from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.History import History
from f5.models.Permission.Permission import Permission

from f5.serializers.History import HistorySerializer as Serializer

from f5.controllers.CustomController import CustomController
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class HistoryLogsController(CustomController):
    @staticmethod
    def get(request: Request) -> Response:
        allUsersHistory = False
        data = dict()
        itemData = {"data": dict()}

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="historyComplete_get") or user["authDisabled"]:
                allUsersHistory = True

            Log.actionLog("History log", user)

            itemData["data"]["items"] = History.list(user["username"], allUsersHistory)
            data["data"] = Serializer(itemData).data["data"]
            data["href"] = request.get_full_path()

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
