from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.ASM.Policy import Policy
from f5.models.Permission.Permission import Permission

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5PolicyApplyController(CustomController):
    @staticmethod
    def post(request: Request, assetId: int, policyId: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="asm_policy_apply_post", assetId=assetId) or user["authDisabled"]:
                Log.actionLog("ASM policy apply", user)
                Log.actionLog("User data: "+str(request.data), user)

                lock = Lock("asm-policy", locals(), policyId)
                if lock.isUnlocked():
                    lock.lock()

                    Policy(assetId=assetId, id=policyId).apply()

                    httpStatus = status.HTTP_201_CREATED
                    lock.release()
                else:
                    httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            if "serializer" in locals():
                Lock("asm-policy", locals(), policyId).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
