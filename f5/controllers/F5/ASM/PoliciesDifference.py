from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.ASM.Policy import Policy
from f5.models.Permission.Permission import Permission

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5ASMPoliciesDifferenceController(CustomController):
    @staticmethod
    def get(request: Request, sourceAssetId: int, destinationAssetId: int, sourcePolicyId: str, destinationPolicyId: str) -> Response:
        data = dict()
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)

        try:
            #if Permission.hasUserPermission(groups=user["groups"], action="asm_policy_differences_get") or user["authDisabled"]:
            if True:
                Log.actionLog("Policy merge", user)

                lock = Lock("asm-policy", locals())
                if lock.isUnlocked():
                    lock.lock()

                    importedPolicyId = Policy.externalPolicyImport(sourceAssetId, destinationAssetId, sourcePolicyId, cleanupPreviouslyImportedPolicy=True)
                    differences = Policy.differences(
                        destinationAssetId=destinationAssetId,
                        destinationPolicyId=destinationPolicyId,
                        sourceAssetId=sourceAssetId,
                        sourcePolicyId=sourcePolicyId,
                        importedPolicyId=importedPolicyId
                    )

                    data = {
                        "data": differences,
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
            Lock("asm-policy", locals()).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })
