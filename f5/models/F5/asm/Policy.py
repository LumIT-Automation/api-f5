import re

from typing import List

from f5.models.Asset.Asset import Asset
from f5.models.F5.asm.backend.Policy import Policy as Backend

from f5.helpers.Exception import CustomException


class Policy:
    def __init__(self, assetId: int, id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.id: str = id
        self.name: str = ""



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self, silent: bool = False) -> dict:
        try:
            i = Backend.info(self.assetId, self.id, silent=silent)
            i["assetId"] = self.assetId

            return i
        except Exception as e:
            raise e



    def delete(self, silent: bool = False) -> None:
        try:
            Backend.delete(self.assetId, self.id, silent=silent)
            del self
        except Exception as e:
            raise e



    def apply(self, silent: bool = False) -> None:
        try:
            Backend.apply(self.assetId, self.id, silent=silent)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int) -> List[dict]:
        try:
            l = Backend.list(assetId)
            for el in l:
                el["assetId"] = assetId

            return l
        except Exception as e:
            raise e



    @staticmethod
    def externalPolicyImport(sourceAssetId: int, destAssetId: int, sourcePolicyId: str, cleanupPreviouslyImportedPolicy: bool = False) -> dict:
        importedPolicyId = ""

        try:
            # Import sourcePolicyId from source asset into destination asset with destinationPolicyName.
            sourcePolicyName = Policy(assetId=sourceAssetId, id=sourcePolicyId).info(silent=True)["name"]
            destinationPolicyName = sourcePolicyName + ".imported-from-" + Asset(assetId=sourceAssetId).fqdn

            l = [(el["name"], el["id"])
                 for el in Policy.list(assetId=destAssetId) if el["name"] == destinationPolicyName] # list of 1 tuple if policy exists, or [].

            try:
                # If destinationPolicyName already exists in policies' list,
                # delete or raise exception, depending on cleanupPreviouslyImportedPolicy.
                if destinationPolicyName == l[0][0]:
                    if cleanupPreviouslyImportedPolicy:
                        Policy(assetId=destAssetId, id=l[0][1]).delete(silent=True)
                    else:
                        raise CustomException(status=400, payload={
                            "F5": f"duplicate policy {destinationPolicyName} on destination asset, please cleanup first"})
            except IndexError:
                pass

            # Load policy content for sourcePolicyId on sourceAssetId.
            sourcePolicyContent = Backend.downloadPolicyFileFacade(sourceAssetId, sourcePolicyId, cleanup=True)
            if sourcePolicyContent:
                # Import policy on destination asset.
                importedPolicy = Backend.importPolicyFacade(
                    assetId=destAssetId,
                    policyContent=sourcePolicyContent,
                    newPolicyName=destinationPolicyName,
                    cleanup=True
                )

                matches = re.search(r"(?<=policies\/)(.*)(?=\?)", importedPolicy.get("policyReference", {}).get("link", ""))
                if matches:
                    importedPolicyId = str(matches.group(1)).strip()

                return {
                    "id": importedPolicyId,
                    "message": importedPolicy.get("message", {})
                }
            else:
                raise CustomException(status=400, payload={"F5": "Empty source policy"})
        except Exception as e:
            raise e



    @staticmethod
    def differences(sourceAssetId: int, destinationAssetId: int, destinationPolicyId: str, sourcePolicyId: str, importedPolicyId: str) -> dict:
        try:
            if destinationPolicyId and importedPolicyId:
                diffReferenceId = Backend.createDiffFacade(destinationAssetId, destinationPolicyId, importedPolicyId)
                differences = Backend.showDifferencesFacade(sourceAssetId, sourcePolicyId, destinationAssetId, diffReferenceId)

                return {
                    "sourcePolicy": {
                        "assetId": sourceAssetId,
                        "id": sourcePolicyId,
                        "name": Policy(assetId=sourceAssetId, id=sourcePolicyId).info(silent=True)["name"]
                    },

                    "importedPolicy": {
                        "assetId": destinationAssetId,
                        "id": importedPolicyId,
                        "name": Policy(assetId=destinationAssetId, id=importedPolicyId).info(silent=True)["name"]
                    },

                    "destinationPolicy": {
                        "assetId": destinationAssetId,
                        "id": destinationPolicyId,
                        "name": Policy(assetId=destinationAssetId, id=destinationPolicyId).info(silent=True)["name"]
                    },

                    "diffReferenceId": diffReferenceId,
                    "differences": differences
                }
            else:
                raise CustomException(status=400, payload={"F5": "No data to process"})
        except Exception as e:
            raise e



    @staticmethod
    def mergeDifferences(assetId: int, destinationPolicyId: str, diffReferenceId: str, mergeDiffsIds: list, deleteDiffsOnDestination: dict) -> None:
        try:
            Backend.diffMergeFacade(
                assetId=assetId,
                destinationPolicyId=destinationPolicyId,
                diffReferenceId=diffReferenceId,
                mergeDiffsIds=mergeDiffsIds,
                deleteDiffsOnDestination=deleteDiffsOnDestination
            )
        except Exception as e:
            raise e
