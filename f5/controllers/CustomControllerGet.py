from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.CheckPermissionFacade import CheckPermissionFacade

from f5.controllers.CustomControllerBase import CustomControllerBase

from f5.helpers.Lock import Locker
from f5.helpers.Conditional import Conditional
from f5.helpers.Log import Log


########################################################################################################################
# Info
########################################################################################################################

class CustomControllerF5GetInfo(CustomControllerBase):
    def __init__(self, subject: str, *args, **kwargs):
        self.subject = subject



    def getInfo(self, request: Request, actionCallback: Callable, objectName: str, assetId: int = 0, partitionName: str = "", objectType: str = "", Serializer: Callable = None, parentSubject: str = "", parentName: str = "") -> Response:
        Serializer = Serializer or None

        action = self.subject + "_get" # example: host_get.
        actionLog = f"{self.subject.capitalize()} {objectType} - info {partitionName} {objectName}".replace("  ", " ")
        httpStatus = None

        # Example:
        #   subject: node
        #   action: node_get

        data = dict()
        etagCondition = {"responseEtag": ""}
        workflowId = request.headers.get("workflowId", "")  # a correlation id.
        checkWorkflowPermission = request.headers.get("checkWorkflowPermission", "")

        try:
            user = CustomControllerBase.loggedUser(request)
            if CheckPermissionFacade.hasUserPermission(groups=user["groups"], action=action, assetId=assetId, partition=partitionName, isWorkflow=bool(workflowId)) or user["authDisabled"]:
                if workflowId and checkWorkflowPermission:
                    httpStatus = status.HTTP_204_NO_CONTENT
                else:
                    Log.actionLog(actionLog, user)

                    locker = Locker(self.subject, locals(), objectName, workflowId, parentSubject, parentName)
                    if locker.isUnlocked():
                        locker.lock()

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
                            locker.release()
                    else:
                        data = None
                        httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN

        except Exception as e:
            if not workflowId:
                Locker(objectClass=self.subject, o=locals(), item=objectName, parentObjectClass=parentSubject, parentItem=parentName).release()

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



    def getList(self, request: Request, actionCallback: Callable, assetId: int = 0, partitionName: str = "", objectType: str = "", Serializer: Callable = None, customCallback: bool = False, parentSubject: str = "", parentName: str = "") -> Response:
        Serializer = Serializer or None
        data = {"data": dict()}
        etagCondition = {"responseEtag": ""}
        workflowId = request.headers.get("workflowId", "")  # a correlation id.
        checkWorkflowPermission = request.headers.get("checkWorkflowPermission", "")
        
        if self.subject[-1:] == "y":
            action = self.subject[:-1] + "ies_get" # example: categories_get.
        else:
            action = self.subject + "s_get" # example: host_get.
        actionLog = f"{self.subject.capitalize()} {objectType} - list {partitionName}".replace("  ", " ")

        # Example: 
        #   subject: host
        #   action: hosts_get

        try:
            user = CustomControllerBase.loggedUser(request)
            if CheckPermissionFacade.hasUserPermission(groups=user["groups"], action=action, assetId=assetId, partition=partitionName, isWorkflow=bool(workflowId)) or user["authDisabled"]:
                if workflowId and checkWorkflowPermission:
                    httpStatus = status.HTTP_204_NO_CONTENT
                else:
                    Log.actionLog(actionLog, user)

                    locker = Locker(objectClass=self.subject, o=locals(), workflowId=workflowId, parentObjectClass=parentSubject, parentItem=parentName)
                    if locker.isUnlocked():
                        locker.lock()

                        if customCallback:
                            data = actionCallback()
                        else:
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
                            locker.release()
                    else:
                        data = None
                        httpStatus = status.HTTP_423_LOCKED
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            if not workflowId:
                Locker(self.subject, locals()).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "ETag": etagCondition["responseEtag"],
            "Cache-Control": "must-revalidate"
        })
