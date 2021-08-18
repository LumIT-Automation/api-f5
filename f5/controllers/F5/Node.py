from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Node import Node
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.Node import F5NodeSerializer as Serializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Lock import Lock
from f5.helpers.Log import Log


class F5NodeController(CustomController):
    @staticmethod
    def delete(request: Request, assetId: int, partitionName: str, nodeName: str) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="node_delete", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Node deletion", user)

                lock = Lock("node", locals(), nodeName)
                if lock.isUnlocked():
                    lock.lock()

                    node = Node(assetId, partitionName, nodeName)
                    node.delete()

                    httpStatus = status.HTTP_200_OK
                    lock.release()
                else:
                    httpStatus = status.HTTP_423_LOCKED
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            Lock("node", locals(), locals()["nodeName"]).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    @staticmethod
    def patch(request: Request, assetId: int, partitionName: str, nodeName: str) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="node_patch", assetId=assetId, partitionName=partitionName) or user["authDisabled"]:
                Log.actionLog("Node modification", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = Serializer(data=request.data, partial=True)
                if serializer.is_valid():
                    data = serializer.validated_data["data"]

                    lock = Lock("node", locals(), nodeName)
                    if lock.isUnlocked():
                        lock.lock()

                        node = Node(assetId, partitionName, nodeName)
                        node.modify(data)

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
            Lock("node", locals(), locals()["nodeName"]).release()

            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
