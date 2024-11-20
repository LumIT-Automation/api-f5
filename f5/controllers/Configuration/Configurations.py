from rest_framework.request import Request
from rest_framework.response import Response

from f5.controllers.CustomControllerGet import CustomControllerF5GetList
from f5.controllers.CustomControllerPost import CustomControllerF5Create

from f5.models.Configuration.Configuration import Configuration

from f5.serializers.Configuration.Configurations import ConfigurationsSerializer
from f5.serializers.Configuration.Configuration import ConfigurationSerializer
from f5.helpers.Exception import CustomException


class ConfigurationsController(CustomControllerF5GetList, CustomControllerF5Create):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="configuration", *args, **kwargs)



    def get(self, request: Request) -> Response:
        configType = list()

        try:
            if 'configType' in request.GET:
                for cType in dict(request.GET)["configType"]:
                    configType.append(cType)

        except Exception as e:
            raise CustomException(status=400, payload={"F5": "Bad url parameter."})


        return self.getList(
            request=request,
            actionCallback=lambda: Configuration.list(configType=configType),
            Serializer=ConfigurationsSerializer
        )



    def post(self, request: Request) -> Response:
        return self.create(
            request=request,
            Serializer=ConfigurationSerializer,
            actionCallback=lambda data: Configuration.add(data)
        )
