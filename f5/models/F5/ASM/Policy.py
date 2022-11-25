from typing import List

from f5.models.F5.ASM.backend.Policy import Policy as Backend


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
    def importPolicy(assetSrcId: int, assetDstId: int, sourcePolicyId: str):
        try:
            policyName = Policy(assetId=assetSrcId, id=sourcePolicyId).info(silent=True)["name"]

            Backend.importFromLocalFile(
                assetId=assetSrcId,
                filename=Backend.uploadPolicyData(
                    assetId=assetDstId,
                    policyContent=Backend.downloadPolicyFile(
                        assetSrcId,
                        Backend.createExportFile(assetSrcId, sourcePolicyId),
                        cleanup=True
                    )
                ),
                name=policyName + ".imported-from-target",
                cleanup=True
            )
        except Exception as e:
            raise e
