from rest_framework.request import Request
from rest_framework.response import Response

from f5.controllers.CustomControllerGet import CustomControllerF5GetInfo
from f5.controllers.CustomControllerDelete import CustomControllerF5Delete
from f5.controllers.CustomControllerPatch import CustomControllerF5Update

from f5.models.Configuration.Configuration import Configuration

from f5.serializers.Configuration.Configuration import ConfigurationSerializer as Serializer


class ConfigurationController(CustomControllerF5GetInfo, CustomControllerF5Delete, CustomControllerF5Update):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="configuration", *args, **kwargs)


    def get(self, request: Request, configId: int) -> Response:
        return self.getInfo(
            request=request,
            actionCallback=lambda: Configuration(id=configId).repr(),
            objectName="configuration",
            Serializer=Serializer
        )



    def delete(self, request: Request, configId: int) -> Response:
        return self.remove(
            request=request,
            actionCallback=lambda: Configuration(id=configId).delete(),
            objectName="configuration",
        )



    def patch(self, request: Request, configId: int) -> Response:
        return self.modify(
            request=request,
            assetId=0,
            Serializer=Serializer,
            actionCallback=lambda data: Configuration(id=configId).modify(data),
            objectName="configuration",
        )
