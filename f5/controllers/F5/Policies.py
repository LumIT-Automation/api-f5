from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Policy import Policy
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.Policies import F5PoliciesSerializer as PoliciesSerializer
from f5.serializers.F5.Policy import F5PolicySerializer as PolicySerializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5PoliciesController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int, partitionName: str) -> Response:
        data = dict()
        itemData = dict()
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="policies_get", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Policies list", user)

                lock = Lock("policy", locals())
                if lock.isUnlocked():
                    lock.lock()

                    itemData["items"] = Policy.list(assetId, partitionName)
                    serializer = PoliciesSerializer(data=itemData)
                    if serializer.is_valid():
                        data["data"] = serializer.validated_data
                        data["href"] = request.get_full_path()

                        # Check the response's ETag validity (against client request).
                        conditional = Conditional(request)
                        etagCondition = conditional.responseEtagFreshnessAgainstRequest(data["data"])
                        if etagCondition["state"] == "fresh":
                            data = None
                            httpStatus = status.HTTP_304_NOT_MODIFIED
                        else:
                            httpStatus = status.HTTP_200_OK
                    else:
                        httpStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
                        data = {
                            "F5": {
                                "error": str(serializer.errors)
                            }
                        }

                        Log.log("Upstream data incorrect: "+str(serializer.errors))

                    lock.release()
                else:
                    data = None
                    httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN

        except Exception as e:
            Lock("policy", locals()).release()
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @staticmethod
    def post(request: Request, assetId: int, partitionName: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="policies_post", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Policy addition", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = PolicySerializer(data=request.data["data"])
                if serializer.is_valid():
                    data = serializer.validated_data
                    data["partition"] = partitionName

                    lock = Lock("policy", locals(), data["name"])
                    if lock.isUnlocked():
                        lock.lock()

                        Policy.add(assetId, data)

                        httpStatus = status.HTTP_201_CREATED
                        lock.release()
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
                Lock("policy", locals(), locals()["serializer"].data["name"]).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
