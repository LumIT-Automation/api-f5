from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.CheckPermissionFacade import CheckPermissionFacade

from f5.controllers.CustomControllerBase import CustomControllerBase

from f5.helpers.Lock import Locker
from f5.helpers.Log import Log


class CustomControllerF5Update(CustomControllerBase):
    def __init__(self,  subject: str, *args, **kwargs):
        self.subject = subject


    def modify(self, request: Request, actionCallback: Callable, objectName: str, assetId: int = 0, partition: str = "", objectType: str = "", Serializer: Callable = None, parentSubject: str = "", parentName: str = "") -> Response:
        Serializer = Serializer or None

        action = self.subject + "_patch"
        actionLog = f"{self.subject.capitalize()} {objectType} - modification: {partition} {objectName}".replace("  ", " ")
        lockedObjectClass = self.subject + objectType
        httpStatus = None

        # Example:
        #   subject: node
        #   action: node_patch
        #   lockedObjectClass: node

        data = None
        response = None
        workflowId = request.headers.get("workflowId", "")  # a correlation id.
        checkWorkflowPermission = request.headers.get("checkWorkflowPermission", "")


        try:
            user = CustomControllerBase.loggedUser(request)
            if CheckPermissionFacade.hasUserPermission(groups=user["groups"], action=action, assetId=assetId, partition=partition, isWorkflow=bool(workflowId)) or user["authDisabled"]:
                if workflowId and checkWorkflowPermission:
                    httpStatus = status.HTTP_204_NO_CONTENT
                else:
                    Log.actionLog(actionLog, user)
                    Log.actionLog("User data: " + str(request.data), user)

                    if Serializer:
                        serializer = Serializer(data=request.data.get("data", {}), partial=True)
                        if serializer.is_valid():
                            data = serializer.validated_data
                        else:
                            httpStatus = status.HTTP_400_BAD_REQUEST
                            response = {
                                "F5": {
                                    "error": str(serializer.errors)
                                }
                            }
                            Log.actionLog("User data incorrect: " + str(response), user)
                    else:
                        data = request.data.get("data", {})

                    if data:
                        locker = Locker(lockedObjectClass, locals(), objectName, workflowId, parentSubject, parentName)
                        if locker.isUnlocked():
                            locker.lock()

                            actionCallback(data)
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

