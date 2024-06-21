from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.ltm.Pool import Pool
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.ltm.PoolMember import F5PoolMemberSerializer as Serializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


class F5PoolMemberController(CustomController):
    @staticmethod
    def get(request: Request, assetId: int, partitionName: str, poolName: str, poolMemberName: str) -> Response:
        data = dict()
        poolSubPath, pool = poolName.rsplit('~', 1) if '~' in poolName else ['', poolName]; poolSubPath = poolSubPath.replace('~', '/')
        memberSubPath, poolMember = poolMemberName.rsplit('~', 1) if '~' in poolMemberName else ['', poolMemberName]; memberSubPath = memberSubPath.replace('~', '/')
        etagCondition = { "responseEtag": "" }

        user = CustomController.loggedUser(request)
        workflowId = request.headers.get("workflowId", "") # a correlation id.
        checkWorkflowPermission = request.headers.get("checkWorkflowPermission", "")

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="poolMember_get", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                if workflowId and checkWorkflowPermission:
                    httpStatus = status.HTTP_204_NO_CONTENT
                else:
                    Log.actionLog("Pool member information", user)

                    # Locking logic for pool member and pool.
                    lockp = Lock("pool", locals(), poolName)
                    lockpm = Lock("poolMember", locals(), poolMemberName)
                    if lockp.isUnlocked() and lockpm.isUnlocked():
                        lockp.lock()
                        lockpm.lock()

                        data = {
                            "data": CustomController.validate(
                                Pool(assetId, pool, partitionName, poolSubPath).getMember(poolMember, memberSubPath).info(),
                                Serializer,
                                "value"
                            ),
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
            #Lock("poolMember", locals(), poolMemberName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



    @staticmethod
    def delete(request: Request, assetId: int, partitionName: str, poolName: str, poolMemberName: str) -> Response:
        poolSubPath, pool = poolName.rsplit('~', 1) if '~' in poolName else ['', poolName]; poolSubPath = poolSubPath.replace('~', '/')
        memberSubPath, poolMember = poolMemberName.rsplit('~', 1) if '~' in poolMemberName else ['', poolMemberName]; poolSubPath = poolSubPath.replace('~', '/')
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="poolMember_delete", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Pool members deletion", user)

                # Locking logic for pool member and pool.
                lockp = Lock("pool", locals(), poolName)
                lockpm = Lock("poolMember", locals(), poolMemberName)
                if lockp.isUnlocked() and lockpm.isUnlocked():
                    lockp.lock()
                    lockpm.lock()

                    Pool(assetId, pool, partitionName, poolSubPath).getMember(poolMember, memberSubPath).delete()

                    httpStatus = status.HTTP_200_OK
                    lockp.release()
                    lockpm.release()
                else:
                    httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("pool", locals(), poolName).release()
            Lock("poolMember", locals(), poolMemberName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    @staticmethod
    def patch(request: Request, assetId: int, partitionName: str, poolName: str, poolMemberName: str) -> Response:
        response = None
        poolSubPath, pool = poolName.rsplit('~', 1) if '~' in poolName else ['', poolName]; poolSubPath = poolSubPath.replace('~', '/')
        memberSubPath, poolMember = poolMemberName.rsplit('~', 1) if '~' in poolMemberName else ['', poolMemberName]; poolSubPath = poolSubPath.replace('~', '/')
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="poolMember_patch", assetId=assetId, partition=partitionName) or user["authDisabled"]:
                Log.actionLog("Pool members modify", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = Serializer(data=request.data["data"], partial=True)
                if serializer.is_valid():
                    data = serializer.validated_data

                    lockp = Lock("pool", locals(), poolName)
                    lockpm = Lock("poolMember", locals(), poolMemberName)
                    if lockp.isUnlocked() and lockpm.isUnlocked():
                        lockp.lock()
                        lockpm.lock()

                        Pool(assetId, pool, partitionName, poolSubPath).getMember(poolMember, memberSubPath).modify(data)

                        httpStatus = status.HTTP_200_OK
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
            Lock("pool", locals(), poolName).release()
            Lock("poolMember", locals(), poolMemberName).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
