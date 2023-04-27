from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.Asset.Asset import Asset
from f5.models.Permission.Permission import Permission

from f5.serializers.Asset.AssetDrAssets import F5AssetDrAssetsSerializer as AssetSerializer

from f5.controllers.CustomController import CustomController
from f5.helpers.Log import Log


class F5AssetAssetsDrController(CustomController):
    @staticmethod
    def post(request: Request, assetId: int) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="assets_post") or user["authDisabled"]:
                Log.actionLog("Asset's disaster recovery related asset addition", user)

                serializer = AssetSerializer(data=request.data["data"])
                if serializer.is_valid():
                    data = serializer.validated_data
                    Asset(assetId).drAdd(drAssetId=data["assetDrId"], enabled=data["enabled"])

                    httpStatus = status.HTTP_201_CREATED
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
