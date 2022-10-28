from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.IdentityGroup import IdentityGroup
from f5.models.Permission.Role import Role
from f5.models.Permission.Partition import Partition
from f5.models.Permission.Permission import Permission

from f5.serializers.Permission.Permission import PermissionSerializer as Serializer

from f5.controllers.CustomController import CustomController

from f5.helpers.Exception import CustomException
from f5.helpers.Log import Log


class PermissionController(CustomController):
    @staticmethod
    def delete(request: Request, permissionId: int) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="permission_identityGroup_delete") or user["authDisabled"]:
                Log.actionLog("Permission deletion", user)

                Permission(permissionId).delete()

                httpStatus = status.HTTP_200_OK
            else:
                httpStatus = status.HTTP_403_FORBIDDEN

        except Exception as e:
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    @staticmethod
    def patch(request: Request, permissionId: int) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="permission_identityGroup_patch") or user["authDisabled"]:
                Log.actionLog("Permission modification", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = Serializer(data=request.data["data"], partial=True)
                if serializer.is_valid():
                    data = serializer.validated_data

                    assetId = data["partition"]["id_asset"]
                    group = data["identity_group_identifier"]
                    role = data["role"]
                    partitionName = data["partition"]["name"]

                    # Get existent or new partition.
                    try:
                        partition = Partition(assetId=assetId, name=partitionName)
                    except CustomException as e:
                        if e.status == 404:
                            try:
                                # If domain does not exist, create it (on Permissions database).
                                partition = Partition(
                                    id=Partition.add(assetId, partitionName, role)
                                )
                            except Exception:
                                raise e
                        else:
                            raise e

                    Permission(permissionId).modify(
                        identityGroup=IdentityGroup(identityGroupIdentifier=group),
                        role=Role(role=role),
                        partition=partition
                    )

                    httpStatus = status.HTTP_200_OK
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
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(response, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
