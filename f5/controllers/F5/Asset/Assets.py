from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from f5.models.F5.Asset.Asset import Asset
from f5.models.Permission.Permission import Permission

from f5.serializers.F5.Asset.Assets import F5AssetsSerializer as AssetsSerializer
from f5.serializers.F5.Asset.Asset import F5AssetSerializer as AssetSerializer

from f5.controllers.CustomController import CustomController
from f5.helpers.Log import Log


class F5AssetsController(CustomController):
    @staticmethod
    def get(request: Request) -> Response:
        allowedData = list()
        includeDr = False

        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="assets_get") or user["authDisabled"]:
                Log.actionLog("Asset list", user)

                if "includeDr" in request.GET:
                    includeDr = True

                itemData = Asset.dataList(includeDr=includeDr)
                for p in itemData:
                    # Filter assets' list basing on actual permissions.
                    if Permission.hasUserPermission(groups=user["groups"], action="assets_get", assetId=p["id"]) or user["authDisabled"]:
                        allowedData.append(p)

                data = {
                    "data": {
                        "items": CustomController.validate(
                            allowedData,
                            AssetsSerializer,
                            "list"
                        )
                    },
                    "href": request.get_full_path()
                }

                httpStatus = status.HTTP_200_OK
            else:
                data = None
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(data, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })



    @staticmethod
    def post(request: Request) -> Response:
        response = None
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="assets_post") or user["authDisabled"]:
                Log.actionLog("Asset addition", user)

                serializer = AssetSerializer(data=request.data["data"])
                if serializer.is_valid():
                    Asset.add(serializer.validated_data)

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



    @staticmethod
    def delete(request: Request) -> Response:
        user = CustomController.loggedUser(request)

        try:
            if Permission.hasUserPermission(groups=user["groups"], action="asset_delete") or user["authDisabled"]:
                Log.actionLog("Purge all assets", user)

                Asset.purgeAll()

                httpStatus = status.HTTP_200_OK
            else:
                httpStatus = status.HTTP_403_FORBIDDEN
        except Exception as e:
            data, httpStatus, headers = CustomController.exceptionHandler(e)
            return Response(data, status=httpStatus, headers=headers)

        return Response(None, status=httpStatus, headers={
            "Cache-Control": "no-cache"
        })
