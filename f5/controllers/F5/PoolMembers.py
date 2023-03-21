from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Pool import Pool
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.PoolMembers import F5PoolMembersSerializer as PoolMembersSerializer
from f5.serializers.F5.PoolMember import F5PoolMemberSerializer as PoolMemberSerializer

from f5.controllers.CustomController import CustomController

from f5.helpers.AssetDr import AssetDr
from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5PoolMembersController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int, partitionName: str, poolName: str) -> Response:
        data = dict()
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="poolMembers_get", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Pool members list", user)

                # Locking logic for pool member and pool.
                lockp = Lock("pool", locals(), poolName)
                lockpm = Lock("poolMember", locals())
                if lockp.isUnlocked() and lockpm.isUnlocked():
                    lockp.lock()
                    lockpm.lock()

                    data = {
                        "data": {
                            "items": CustomController.validate(
                                Pool(assetId, partitionName, poolName).members(),
                                PoolMembersSerializer,
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

                    lockp.release()
                    lockpm.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("pool", locals(), poolName).release()
            Lock("poolMember", locals()).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @staticmethod
    @AssetDr
    def post(request: Request, assetId: int, partitionName: str, poolName: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="poolMembers_post", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Add node/port to pool (create pool member)", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = PoolMemberSerializer(data=request.data["data"])
                if serializer.is_valid():
                    data = serializer.validated_data
                    if "state" in data:
                        data["State"] = data["state"] # curious F5 field's name.
                        del(data["state"])

                    # Locking logic for pool member and pool.
                    lockp = Lock("pool", locals(), poolName)
                    lockpm = Lock("poolMember", locals(), data["name"])
                    if lockp.isUnlocked() and lockpm.isUnlocked():
                        lockp.lock()
                        lockpm.lock()

                        Pool(assetId, partitionName, poolName).addMember(data)

                        httpStatus = status.HTTP_201_CREATED
                        lockp.release()
                        lockpm.release()
                    else:
                        httpStatus = status.HTTP_423_LOCKED
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
            if "serializer" in locals():
                Lock("poolMember", locals(), locals()["serializer"].data["name"]).release()
                Lock("pool", locals(), poolName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
