import functools

from django.urls import resolve
from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.History.ActionHistory import ActionHistory

from f5.controllers.CustomController import CustomController
from f5.helpers.Log import Log


class HistoryLog:
    def __init__(self, wrappedMethod: callable, *args, **kwargs) -> None:
        self.wrappedMethod = wrappedMethod
        self.assetId: int = 0
        self.action: str = "" # dispatcher path "name" (defined in urls.py).



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def __call__(self, request: Request, **kwargs):
        @functools.wraps(request)
        def wrapped():
            try:
                # Perform the request to the primary asset.
                response = self.wrappedMethod(request, **kwargs)

                HistoryLog.__historyPrepare(
                    assetId=int(kwargs["assetId"]),
                    action=resolve(request.path).url_name + '_' + request.method.lower(),
                    response=response,
                    user=CustomController.loggedUser(request)["username"]
                )

                return response
            except Exception as e:
                raise e

        return wrapped()



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __historyPrepare(assetId: int, action: str, response: Response, user: str) -> None:
        try:
            ActionHistory.add({
                "asset_id":  int(assetId),
                "action": action,
                "response_status": int(response.status_code),
                "username": user
            })
        except Exception:
            pass
