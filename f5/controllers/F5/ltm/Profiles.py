import threading

from rest_framework.request import Request
from rest_framework.response import Response

from f5.models.F5.ltm.Profile import Profile

from f5.serializers.F5.ltm.Profiles import F5ProfilesSerializer as ProfilesSerializer
from f5.serializers.F5.ltm.Profile import F5ProfileSerializer as ProfileSerializer

from f5.controllers.CustomControllerGet import CustomControllerF5GetList
from f5.controllers.CustomControllerPost import CustomControllerF5Create


class F5ProfilesController(CustomControllerF5GetList, CustomControllerF5Create):
    def __init__(self, *args, **kwargs):
        super().__init__(subject="profile", *args, **kwargs)



    def get(self, request: Request, assetId: int, partitionName: str, profileType: str = "") -> Response:
        def actionCallback():
            data = {"data": dict()}
            itemData = dict()

            if profileType:
                if profileType != "ANY":
                    # Profiles' list of that type.
                    # F5 treats profile type as a sub-object instead of a property. Odd.
                    itemData["items"] = [r.repr() for r in Profile.list(assetId, partitionName, profileType)]
                    data["data"] = ProfilesSerializer(itemData).data
                else:
                    profileTypes = Profile.types(assetId, partitionName)

                    # The threading way.
                    # This requires a consistent throttle on remote appliance.
                    def profilesListOfType(pType):
                        itemData["items"] = [r.repr() for r in Profile.list(assetId, partitionName, pType)]
                        data["data"][pType] = ProfilesSerializer(itemData).data

                    workers = [threading.Thread(target=profilesListOfType, args=(m,)) for m in profileTypes]
                    for w in workers:
                        w.start()
                    for w in workers:
                        w.join()
            else:
                # Profiles' types list.
                # No need for a serializer: just a list of strings.
                data["data"]["items"] = Profile.types(assetId, partitionName)

            data["href"] = request.get_full_path()
            return data


        return self.getList(
            request=request,
            actionCallback=actionCallback,
            assetId=assetId,
            partition=partitionName,
            objectType=profileType,
            customCallback=True
        )



    def post(self, request: Request, assetId: int, partitionName: str, profileType: str) -> Response:
        def dataFix(data: dict):
            data["partition"] = partitionName
            return data


        return self.create(
            request=request,
            actionCallback=lambda data: Profile.add(assetId, profileType, data),
            assetId=assetId,
            partition=partitionName,
            objectType=profileType,
            Serializer=ProfileSerializer,
            lockItemDataKey="name",
            dataFix=dataFix
        )
