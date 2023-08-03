from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.net.RouteDomain import RouteDomain
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.net.RouteDomains import F5RouteDomainsSerializer as Serializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5RouteDomainsController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int) -> Response:
        data = dict()
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="routedomains_get", assetId=assetId) or user["authDisabled"]:
                Log.actionLog("Root domains list", user)

                lock = Lock("routedomain", locals())
                if lock.isUnlocked():
                    lock.lock()

                    data = {
                        "data": {
                            "items": CustomController.validate(
                                RouteDomain.list(assetId),
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

                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("routedomain", locals()).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })
