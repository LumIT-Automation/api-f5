from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.asm.Policy import Policy
from f5.models.Permission.Permission import Permission

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5PolicyController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int, policyId: str) -> Response:
        data = dict()
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="asm_policy_get", assetId=assetId) or user["authDisabled"]:
                Log.actionLog("ASM policy information", user)

                # Locking logic for pool member and pool.
                lock = Lock("asm-policy", locals(), policyId)
                if lock.isUnlocked():
                    lock.lock()
                    data = {
                        "data": Policy(assetId=assetId, id=policyId).info(),
                        "href": request.get_full_path()
                    }

                    # data = {
                    #     "data": CustomController.validate(
                    #         Policy(assetId=assetId, id=policyId).info(),
                    #         Serializer,
                    #         "value"
                    #     ),
                    #     "href": request.get_full_path()
                    # }

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
            Lock("asm-policy", locals(), policyId).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @staticmethod
    def delete(request: Request, assetId: int, policyId: str) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="asm_policy_delete", assetId=assetId) or user["authDisabled"]:
                Log.actionLog("ASM policy deletion", user)

                lock = Lock("asm-policy", locals(), policyId)
                if lock.isUnlocked():
                    lock.lock()

                    Policy(assetId, policyId).delete()

                    httpStatus = status.HTTP_200_OK
                    lock.release()
                else:
                    httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("asm-policy", locals(), policyId).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
