from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.sys.GlobalSettings import GlobalSettings

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update


class F5GlobalSettingsController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="globalsettings", *args, **kwargs)


    def get(self, request: Request, assetId: int, selfName: str) -> Response:
        return self.getInfo(
            request=request,
            actionCallback=lambda: GlobalSettings(assetId, selfName).info(),
            objectName=selfName,
            assetId=assetId
        )
