from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Permission.IdentityGroup import IdentityGroup
from f5.models.Permission.Permission import Permission

from f5.serializers.Permission.IdentityGroup import IdentityGroupSerializer as GroupSerializer

from f5.controllers.CustomController import CustomController
from f5.helpers.Log import Log


class PermissionIdentityGroupController(CustomController):
    @staticmethod
    def delete(request: Request, identityGroupIdentifier: str) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="permission_identityGroup_delete") or user["authDisabled"]:
                Log.actionLog("Identity group deletion", user)

                ig = IdentityGroup(identityGroupIdentifier)
                ig.delete()

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
    def patch(request: Request, identityGroupIdentifier: str) -> Response:
        response = None
        roles = dict()
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="permission_identityGroup_patch") or user["authDisabled"]:
                Log.actionLog("Identity group modification", user)
                Log.actionLog("User data: "+str(request.data), user)

                serializer = GroupSerializer(data=request.data, partial=True)
                if serializer.is_valid():
                    data = serializer.validated_data["data"]

                    # roles is a dictionary of related roles/partitions,
                    # which is POSTed together with the main identity group item:
                    if "roles_partition" in data:
                        # "roles_partition": {
                        #     "staff": [
                        #         {
                        #             "assetId": 1,
                        #             "partition": "any"
                        #         },
                        #         ...
                        #     ],
                        #     ...
                        # }

                        for k, v in data["roles_partition"].items():
                            roles[k] = v

                        del (data["roles_partition"])

                    # Modify identity group data.
                    ig = IdentityGroup(identityGroupIdentifier)
                    igId = ig.modify(data)

                    # Also, replace associated roles with roles[]' elements.
                    try:
                        # Cleanup existent roles.
                        Permission.cleanup(identityGroupId=igId)
                    except Exception:
                        pass

                    for roleName, partitionsAssetsList in roles.items():
                        for partitionsAssetDict in partitionsAssetsList:
                            try:
                                Permission.add(igId, roleName, partitionsAssetDict["assetId"], partitionsAssetDict["partition"])
                            except Exception:
                                pass

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
