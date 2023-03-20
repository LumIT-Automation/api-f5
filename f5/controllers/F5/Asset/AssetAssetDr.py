from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Asset.Asset import Asset
from f5.models.Permission.Permission import Permission
from f5.serializers.F5.Asset.AssetDrAsset import F5AssetDrAssetSerializer as Serializer

from f5.controllers.CustomController import CustomController
from f5.helpers.Log import Log


class F5AssetAssetDrController(CustomController):
    @staticmethod
    def delete(request: Request, assetId: int, assetDrId: int) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="asset_delete") or user["authDisabled"]:
                Log.actionLog("Asset's disaster recovery related asset deletion", user)

                Asset(assetId).drRemove(assetDrId)

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
    def patch(request: Request, assetId: int, assetDrId: int) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="asset_patch") or user["authDisabled"]:
                Log.actionLog("Asset's disaster recovery related asset enable/disable", user)

                serializer = Serializer(data=request.data["data"], partial=True)
                if serializer.is_valid():
                    data = serializer.validated_data

                    Asset(assetId).drModify(drAssetId=assetDrId, enabled=bool(data["enabled"]))

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
