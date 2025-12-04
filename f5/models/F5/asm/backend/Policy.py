import json
import time

from typing import List

from f5.models.Asset.Asset import Asset
from f5.models.F5.asm.backend.PolicyBase import PolicyBase

from f5.models.F5.asm.backend.PolicyExporter import PolicyExporter
from f5.models.F5.asm.backend.PolicyImporter import PolicyImporter
from f5.models.F5.asm.backend.PolicyDiffManager import PolicyDiffManager

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Exception import CustomException

#/mgmt/tm/asm/policies?$select=name,virtualServers,manualVirtualServers,enforcementMode

class Policy(PolicyBase):

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(assetId: int, id: str, silent: bool = False) -> dict:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/policies/"+id+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=silent
            )

            return api.get()["payload"]
        except Exception as e:
            raise e



    @staticmethod
    def list(assetId: int) -> List[dict]:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/policies/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            return api.get()["payload"]["items"]
        except Exception as e:
            raise e



    @staticmethod
    def delete(assetId: int, id: str, silent: bool = False) -> None:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/policies/"+id+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=silent
            )

            api.delete()
        except Exception as e:
            raise e



    @staticmethod
    def apply(assetId: int, id: str, silent: bool = False) -> None:
        timeout = 3600 # [second]

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/tasks/apply-policy",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=silent
            )

            Policy._log(
                f"[AssetID: {assetId}] Applying policy..."
            )

            taskInformation = api.post(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "policyReference": {
                        "link": "https://localhost/mgmt/tm/asm/policies/" + id
                    }
                })
            )["payload"]

            # Monitor async tasks.
            t0 = time.time()

            while True:
                try:
                    api = ApiSupplicant(
                        endpoint=f5.baseurl + "tm/asm/tasks/apply-policy/" + taskInformation["id"] + "/",
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    )

                    PolicyDiffManager._log(
                        f"[AssetID: {assetId}] Waiting for task to complete..."
                    )

                    taskOutput = api.get()["payload"]
                    taskStatus = taskOutput["status"].lower()
                    if taskStatus == "completed":
                        break
                    if taskStatus == "failure":
                        raise CustomException(status=400, payload={"F5": "Policy apply failed"})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"F5": "Policy apply timed out"})

                    time.sleep(5)
                except KeyError:
                    raise CustomException(status=400, payload={"F5": "Policy apply failed"})
        except Exception as e:
            raise e



    @staticmethod
    def deletePolicyObjects(assetId: int, policyId: str, o: dict) -> None:
        # @todo: create and use models.
        try:
            f5 = Asset(assetId)

            PolicyBase._log(
                f"[AssetID: {assetId}] Deleting objects on policy {policyId}..."
            )

            for k, v in o.items():
                for o in v:
                    api = ApiSupplicant(
                        endpoint=f5.baseurl + "tm/asm/policies/" + policyId + "/" + k + "/" + o + "/",
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify,
                        silent=True
                    )

                    api.delete()
        except Exception as e:
            raise e



    @staticmethod
    def downloadPolicyFileFacade(assetId: int, policyId: str, cleanup: bool = False) -> bytes:
        try:
            return PolicyExporter.downloadPolicyData(
                assetId=assetId,
                localExportFile=PolicyExporter.createExportFile(
                    assetId=assetId,
                    policyId=policyId
                ),
                cleanup=cleanup
            )
        except Exception as e:
            raise e



    @staticmethod
    def importPolicyFacade(assetId: int, policyContent: bytes, newPolicyName: str, cleanup: bool = False) -> dict:
        try:
            return PolicyImporter.importFromLocalFile(
                assetId=assetId,
                localImportFile=PolicyImporter.uploadPolicyData(
                    assetId=assetId,
                    policyContent=policyContent
                ),
                name=newPolicyName,
                cleanup=cleanup
            )
        except Exception as e:
            raise e



    @staticmethod
    def createDiffFacade(assetId: int, destinationPolicyId: str, importedPolicyId: str) -> str:
        try:
            return PolicyDiffManager.createDiff(assetId, destinationPolicyId, importedPolicyId)
        except Exception as e:
            raise e



    @staticmethod
    def showDifferencesFacade(sourceAssetId: int, sourcePolicyId: str, destinationAssetId: int, diffReferenceId: str) -> list:
        try:
            return PolicyDiffManager.listDifferences(sourceAssetId, sourcePolicyId, destinationAssetId, diffReferenceId)
        except Exception as e:
            raise e



    @staticmethod
    def diffMergeFacade(assetId: int, destinationPolicyId: str, diffReferenceId: str, mergeDiffsIds: list, deleteDiffsOnDestination: dict) -> None:
        try:
            # Merge diffs selectively.
            PolicyDiffManager.mergeDifferences(
                assetId=assetId,
                diffReferenceId=diffReferenceId,
                mergeDiffsIds=mergeDiffsIds
            )

            # Also delete only-in-destination user-selected policy objects from destination policy.
            Policy.deletePolicyObjects(
                assetId=assetId,
                policyId=destinationPolicyId,
                o=PolicyDiffManager.getObjectsIdsFromDiffNames(
                    assetId=assetId,
                    policyId=destinationPolicyId,
                    differences=deleteDiffsOnDestination,
                    policyType="destination"
                )
            )
        except Exception as e:
            raise e
