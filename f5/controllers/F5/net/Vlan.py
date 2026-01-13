from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.net.Vlan import Vlan

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update


class F5VlanController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        CustomControllerF5GetInfo.__init__(self, subject="vlan", *args, **kwargs)


    def get(self, request: Request, assetId: int, vlanName: str) -> Response:
        return self.getInfo(
            request=request,
            actionCallback=lambda: Vlan(assetId, vlanName).info(),
            objectName=vlanName,
            assetId=assetId
        )
