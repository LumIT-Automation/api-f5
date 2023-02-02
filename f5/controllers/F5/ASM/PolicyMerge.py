from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.ASM.Policy import Policy
from f5.models.Permission.Permission import Permission

from f5.controllers.CustomController import CustomController

from f5.serializers.F5.ASM.PolicyMerge import F5PolicyMergeSerializer as Serializer

from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5ASMPoliciesMergeController(CustomController):
    @staticmethod
    def post(request: Request, assetId: int, destinationPolicyId: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="asm_policy_merge_post", assetId=assetId) or user["authDisabled"]:
                Log.actionLog("ASM policy merge", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = Serializer(data=request.data["data"])
                if serializer.is_valid():
                    data = serializer.validated_data

                    lock = Lock("asm-policy", locals(), destinationPolicyId)
                    if lock.isUnlocked():
                        lock.lock()

                        Policy.mergeDifferences(
                            assetId=assetId,
                            importedPolicyId=data["importedPolicyId"],
                            destinationPolicyId=destinationPolicyId,
                            ignoreDiffs=data["ignoreDiffs"],
                            deleteDiffsOnDestination=data["deleteDiffsOnDestination"],
                        )

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
            Lock("asm-policy", locals(), destinationPolicyId).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
