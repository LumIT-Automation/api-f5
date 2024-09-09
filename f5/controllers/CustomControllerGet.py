from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.CheckPermissionFacade import CheckPermissionFacade

from f5.controllers.CustomControllerBase import CustomControllerBase

from f5.helpers.Lock import Lock
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


########################################################################################################################
# Info
########################################################################################################################

class CustomControllerF5GetInfo(CustomControllerBase):
    def __init__(self, subject: str, *args, **kwargs):
        self.subject = subject



    def getInfo(self, request: Request, actionCallback: Callable, objectName: str, assetId: int = 0, partition: str = "", objectType: str = "", Serializer: Callable = None, parentSubject: str = "", parentName: str = "") -> Response:
        Serializer = Serializer or None

        action = self.subject + "_get" # example: host_get.
        actionLog = f"{self.subject.capitalize()} {objectType} - info {partition} {objectName}".replace("  ", " ")
        lockedObjectClass = self.subject + objectType # example: host (subject=host) // ruleaccess (subject=rule + type=access).
        lockParent = None
        httpStatus = None

        # Example:
        #   subject: node
        #   action: node_get
        #   lockedObjectClass: node

        data = dict()
        etagCondition = {"responseEtag": ""}
        workflowId = request.headers.get("workflowId", "")  # a correlation id.
        checkWorkflowPermission = request.headers.get("checkWorkflowPermission", "")

        try:
            user = CustomControllerBase.loggedUser(request)
            if CheckPermissionFacade.hasUserPermission(groups=user["groups"], action=action, assetId=assetId, partition=partition, isWorkflow=bool(workflowId)) or user["authDisabled"]:
                if workflowId and checkWorkflowPermission:
                    httpStatus = status.HTTP_204_NO_CONTENT
                else:
                    Log.actionLog(actionLog, user)

                    if parentSubject:
                        lockParent = Lock(parentSubject, locals(), parentName)
                    lock = Lock(lockedObjectClass, locals(), objectName)

                    if lockParent:
                        if lockParent.isUnlocked():
                            lockParent.lock()
                        else:
                            httpStatus = status.HTTP_423_LOCKED

                    if lock.isUnlocked() and httpStatus != status.HTTP_423_LOCKED:
                        lock.lock()

                        data = {
                            "data": CustomControllerBase.validate(actionCallback(), Serializer),
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
                        if not workflowId:
                            lock.release()
                            if lockParent:
                                lockParent.release()
                    else:
                        data = None
                        httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN

        except Exception as e:
            if not workflowId:
                Lock(lockedObjectClass, locals(), objectName).release()
                if parentSubject:
                    Lock(parentSubject, locals(), parentName).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })



########################################################################################################################
# List
########################################################################################################################

class CustomControllerF5GetList(CustomControllerBase):
    def __init__(self, subject: str, *args, **kwargs):
        self.subject = subject



    def getList(self, request: Request, actionCallback: Callable, assetId: int = 0, partition: str = "", objectType: str = "", Serializer: Callable = None) -> Response:
        Serializer = Serializer or None
        data = dict()
        etagCondition = {"responseEtag": ""}
        workflowId = request.headers.get("workflowId", "")  # a correlation id.
        checkWorkflowPermission = request.headers.get("checkWorkflowPermission", "")
        
        if self.subject[-1:] == "y":
            action = self.subject[:-1] + "ies_get" # example: categories_get.
        else:
            action = self.subject + "s_get" # example: host_get.
        actionLog = f"{self.subject.capitalize()} {objectType} - list {partition}".replace("  ", " ")
        lockedObjectClass = self.subject + objectType # example: category // layeraccess.
        
        # Example: 
        #   subject: host
        #   action: hosts_get
        #   lockedObjectClass: host
        try:
            user = CustomControllerBase.loggedUser(request)
            if CheckPermissionFacade.hasUserPermission(groups=user["groups"], action="action", assetId=assetId, partition=partition, isWorkflow=bool(workflowId)) or user["authDisabled"]:
                if workflowId and checkWorkflowPermission:
                    httpStatus = status.HTTP_204_NO_CONTENT
                else:
                    Log.actionLog(actionLog, user)

                    lock = Lock(lockedObjectClass, locals())
                    if lock.isUnlocked():
                        if not workflowId:
                            lock.lock()

                        data = {
                            "data": {
                                "items": CustomControllerBase.validate(actionCallback(), Serializer, many=True)
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

                        if not workflowId:
                            lock.release()
                    else:
                        data = None
                        httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            if not workflowId:
                Lock(lockedObjectClass, locals()).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })
