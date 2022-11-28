from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.ASM.Policy import Policy
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.Node import F5NodeSerializer as Serializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5PolicyMergeController(CustomController):
    @staticmethod
    def put(request: Request, sourceAssetId: int, destinationAssetId: int, policyId: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            #if Permission.hasUserPermission(groups=user["groups"], action="node_patch", assetId=assetId, partition=partitionName) or user["authDisabled"]:
            if True:
                Log.actionLog("Policy merge", user)
                Log.actionLog("User data: "+str(request.data), user)

                #serializer = Serializer(data=request.data["data"], partial=True)
                #if serializer.is_valid():
                if True:
                    #data = serializer.validated_data
                    data = request.data["data"]

                    lock = Lock("asm-policy", locals())
                    if lock.isUnlocked():
                        lock.lock()

                        # response = Policy.showDifferences(
                        #     assetId=destinationAssetId,
                        #     diffReference=Policy.createDifferences(
                        #         assetId=destinationAssetId,
                        #         firstPolicy="https://localhost/mgmt/tm/asm/policies/7oVv7uJjXPLWvk9iYHzbaA",
                        #         secondPolicy=Policy.importPolicy(sourceAssetId, destinationAssetId, policyId, cleanupPreviouslyImportedPolicy=True).get("policyReference", {}).get("link", "")
                        #     ).get("policyDiffReference", {}).get("link", "")
                        # )

                        response = Policy.showDifferences(
                            assetId=destinationAssetId,
                            diffReference="https://localhost/mgmt/tm/asm/policy-diffs/BJHo4B9ZSwPV1ewmzQno_A?ver=16.1.0"
                        )

                        httpStatus = status.HTTP_200_OK
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
            Lock("asm-policy", locals()).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
