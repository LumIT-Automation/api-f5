from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.CheckPermissionFacade import CheckPermissionFacade

from f5.controllers.CustomControllerBase import CustomControllerBase

from f5.helpers.Lock import Locker
from f5.helpers.Log import Log



class CustomControllerF5Delete(CustomControllerBase):
    def __init__(self, subject: str, *args, **kwargs):
        self.subject = subject


    def remove(self, request: Request, actionCallback: Callable, objectName: str, assetId: int = 0, partition: str = "", objectType: str = "", Serializer: Callable = None, parentSubject: str = "", parentName: str = "") -> Response:
        Serializer = Serializer or None

        action = self.subject + "_delete"
        actionLog = f"{self.subject.capitalize()} {objectType} - deletion: {partition} {objectName}".replace("  ", " ")
        lockedObjectClass = self.subject + objectType
        httpStatus = None

        # Example:
        #   subject: node
        #   action: node_delete
        #   lockedObjectClass: node
        workflowId = request.headers.get("workflowId", "")  # a correlation id.
        checkWorkflowPermission = request.headers.get("checkWorkflowPermission", "")

        try:
            user = CustomControllerBase.loggedUser(request)
            if CheckPermissionFacade.hasUserPermission(groups=user["groups"], action=action, assetId=assetId, partition=partition, isWorkflow=bool(workflowId)) or user["authDisabled"]:
                if workflowId and checkWorkflowPermission:
                    httpStatus = status.HTTP_204_NO_CONTENT
                else:
                    Log.actionLog(actionLog, user)

                    locker = Locker(lockedObjectClass, locals(), objectName, workflowId, parentSubject, parentName)
                    if locker.isUnlocked():
                        locker.lock()

                        actionCallback()
                        httpStatus = status.HTTP_200_OK

                        if not workflowId:
                            locker.release()
                    else:
                        httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN

        except Exception as e:
            if not workflowId:
                Locker(objectClass=lockedObjectClass, o=locals(), item=objectName, parentObjectClass=parentSubject, parentItem=parentName).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
