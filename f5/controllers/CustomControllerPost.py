from typing import Callable

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.CheckPermissionFacade import CheckPermissionFacade

from f5.controllers.CustomControllerBase import CustomControllerBase

from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class CustomControllerF5Create(CustomControllerBase):
    def __init__(self,  subject: str, *args, **kwargs):
        self.subject = subject


    def create(self, request: Request, actionCallback: Callable, assetId: int = 0, partition: str = "", objectType: str = "", Serializer: Callable = None, lockItemField: str = "", dataFix: Callable = None, parentSubject: str = "", parentName: str = "") -> Response:
        Serializer = Serializer or None
        httpStatus = None

        if self.subject[-1:] == "y":
            action = self.subject[:-1] + "ies_post"
        else:
            action = self.subject + "s_post"
        actionLog = f"{self.subject.capitalize()} {objectType} - addition: {partition}".replace("  ", " ")
        lockedObjectClass = self.subject + objectType
        lockItem = ""
        lockParent = None

        # Example:
        #   subject: nodes
        #   action: nodes_post
        #   lockedObjectClass: node

        data = None
        response = dict()
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
                        serializer = Serializer(data=request.data.get("data", {}))
                        if serializer.is_valid():
                            data = serializer.validated_data
                            if dataFix: # Adjust data after the serializer.
                                data = dataFix(data)
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
                        if parentSubject:
                            lockParent = Lock(parentSubject, locals(), parentName)
                        if lockItemField:
                            lockItem = data[lockItemField]
                        lock = Lock(lockedObjectClass, locals(), lockItem)

                        if lockParent:
                            if lockParent.isUnlocked():
                                lockParent.lock()
                            else:
                                httpStatus = status.HTTP_423_LOCKED

                        if lock.isUnlocked() and httpStatus != status.HTTP_423_LOCKED:
                            lock.lock()

                            response["data"] = actionCallback(data)
                            if not response["data"]:
                                response = None
                            httpStatus = status.HTTP_201_CREATED

                            if not workflowId:
                                lock.release()
                                if lockParent:
                                    lockParent.release()
                        else:
                            httpStatus = status.HTTP_423_LOCKED
            else:
                response = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            if not workflowId:
                if lockItemField:
                    lockItem = locals()["serializer"].data[lockItemField]
                Lock(lockedObjectClass, locals(), lockItem).release()
                if parentSubject:
                    Lock(parentSubject, locals(), parentName).release()

            data, httpStatus, headers = CustomControllerBase.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
