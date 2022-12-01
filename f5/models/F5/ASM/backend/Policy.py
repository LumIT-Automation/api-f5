from typing import List

from f5.models.F5.Asset.Asset import Asset

from f5.models.F5.ASM.backend.PolicyExporter import PolicyExporter
from f5.models.F5.ASM.backend.PolicyImporter import PolicyImporter
from f5.models.F5.ASM.backend.PolicyDiffManager import PolicyDiffManager

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Log import Log


class Policy:

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
    def delete(assetId: int, id: str) -> None:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/policies/"+id+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.delete()
        except Exception as e:
            raise e



    @staticmethod
    def downloadPolicyFileFacade(assetId: int, policyId: str, cleanup: bool = False) -> str:
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
    def importPolicyFacade(assetId: int, policyContent: str, newPolicyName: str, cleanup: bool = False) -> dict:
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
    def createDiffFacade(assetId: int, destinationPolicyId: str, sourcePolicy: str) -> str:
        try:
            return PolicyDiffManager.createDiff(assetId, destinationPolicyId, sourcePolicy)
        except Exception as e:
            raise e



    @staticmethod
    def showDifferencesFacade(sourceAssetId: int, sourcePolicyId: str, destinationAssetId: int, diffReferenceId: str, sourcePolicyXML: str) -> list:
        try:
            return PolicyDiffManager.listDifferences(sourceAssetId, sourcePolicyId, destinationAssetId, diffReferenceId, sourcePolicyXML)
        except Exception as e:
            raise e
