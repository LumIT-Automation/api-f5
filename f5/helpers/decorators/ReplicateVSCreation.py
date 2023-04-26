import uuid
import functools

from django.conf import settings
from rest_framework.request import Request

from f5.models.F5.Workflow.VirtualServers import VirtualServersWorkflow

from f5.controllers.CustomController import CustomController

from f5.helpers.decorators.ReplicateVSBase import ReplicateVirtualServerBase

from f5.helpers.Log import Log


if not hasattr(settings, "ENABLE_ASSET_DR") or not settings.ENABLE_ASSET_DR:
    def AssetDr(func): # null decorator.
        return func
else:
    class ReplicateVirtualServerCreation(ReplicateVirtualServerBase):
        def __init__(self, wrappedMethod: callable, *args, **kwargs) -> None:
            super().__init__(wrappedMethod, *args, **kwargs)

            self.wrappedMethod = wrappedMethod
            self.request = None
            self.primaryAssetId: int = 0
            self.primaryPartitionName: str = ""



        ####################################################################################################################
        # Public methods
        ####################################################################################################################

        def __call__(self, request: Request, **kwargs):
            @functools.wraps(request)
            def wrapped():
                try:
                    replicaUuid = uuid.uuid4().hex

                    self.request = request
                    self.primaryAssetId = int(kwargs["assetId"])
                    self.primaryPartitionName = kwargs["partitionName"]

                    user = CustomController.loggedUser(request)

                    # Modify the request injecting the __replicaUuid query parameter,
                    # then perform the request to the primary asset.
                    responsePrimary = self.wrappedMethod(
                        ReplicateVirtualServerCreation._forgeRequest(
                            request=request,
                            additionalQueryParams={"__replicaUuid": replicaUuid}
                        ),
                        **kwargs
                    )
                except Exception as e:
                    raise e

                try:
                    # Perform the replica.
                    if responsePrimary.status_code in (200, 201): # reply the action in dr only if it was successful.
                        if "drReplica" in request.query_params and request.query_params["drReplica"]: # reply action in dr only if drReplica=1/true param was passed.
                            for asset in self._listAssetsDr():
                                try:
                                    VirtualServersWorkflow(
                                        assetId=asset["id"],
                                        partitionName=self.primaryPartitionName,
                                        data=self.request.data["data"],
                                        user=user,
                                        replicaUuid=replicaUuid
                                    ).add()
                                except Exception as e:
                                    raise e
                except Exception as e:
                    Log.log("[DR replica] error: " + str(e))

                return responsePrimary

            return wrapped()
