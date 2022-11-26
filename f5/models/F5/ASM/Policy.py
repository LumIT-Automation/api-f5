from typing import List

from f5.models.F5.ASM.backend.Policy import Policy as Backend

from f5.helpers.Exception import CustomException
from f5.helpers.Log import Log


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



    def delete(self):
        try:
            Backend.delete(self.assetId, self.id)
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
    def importPolicy(assetSrcId: int, assetDstId: int, sourcePolicyId: str, cleanupPreviouslyImportedPolicy: bool = False) -> dict:
        try:
            sourcePolicyName = Policy(assetId=assetSrcId, id=sourcePolicyId).info(silent=True)["name"]
            destinationPolicyName = sourcePolicyName + ".imported-from-target"

            l = [(el["name"], el["id"])
                 for el in Policy.list(assetId=assetDstId) if el["name"] == destinationPolicyName] # list of 1 tuple if policy exists, or [].

            try:
                # If destinationPolicyName already exists in policies' list,
                # delete or raise exception, depending on cleanupPreviouslyImportedPolicy.
                if destinationPolicyName == l[0][0]:
                    if cleanupPreviouslyImportedPolicy:
                        Policy(assetId=assetDstId, id=l[0][1]).delete()
                    else:
                        raise CustomException(status=400, payload={
                            "F5": f"duplicate policy {destinationPolicyName}, please cleanup first"})
            except IndexError:
                pass

            return Backend.importPolicyFacade(
                assetId=assetDstId,
                policyContent=Backend.downloadPolicyFileFacade(
                    assetId=assetSrcId,
                    policyId=sourcePolicyId,
                    cleanup=True
                ),
                newPolicyName=destinationPolicyName,
                cleanup=True
            )
        except Exception as e:
            raise e
