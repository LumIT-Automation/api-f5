from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.IdentityGroup import IdentityGroup
from f5.models.Permission.Permission import Permission

from f5.serializers.Permission.IdentityGroups import IdentityGroupsSerializer as GroupsSerializer
from f5.serializers.Permission.IdentityGroup import IdentityGroupSerializer as GroupSerializer

from f5.controllers.CustomController import CustomController
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class PermissionIdentityGroupsController(CustomController):
    @staticmethod
    def get(request: Request) -> Response:
        etagCondition = {"responseEtag": ""}
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="permission_identityGroups_get") or user["authDisabled"]:
                Log.actionLog("Identity group list", user)

                data = {
                    "data": {
                        "items": CustomController.validate(
                            [ig.repr() for ig in IdentityGroup.list()],
                            GroupsSerializer,
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



    @staticmethod
    def post(request: Request) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="permission_identityGroups_post") or user["authDisabled"]:
                Log.actionLog("Identity group addition", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = GroupSerializer(data=request.data["data"])
                if serializer.is_valid():
                    validatedData = serializer.validated_data
                    IdentityGroup.add(validatedData)

                    httpStatus = status.HTTP_201_CREATED
                else:
                    httpStatus = status.HTTP_400_BAD_REQUEST
                    response = {
                        "F5": {
                            "error": str(serializer.errors)
                        }
                    }

                    Log.actionLog("User data incorrect: "+str(response), user)
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
