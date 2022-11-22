from typing import List, Dict, Union

from f5.models.F5.ASM.backend.Policy import Policy as Backend


Link: Dict[str, str] = {
    "link": ""
}

RulesReference: Dict[str, Union[str, bool]] = {
    "link": "",
    "isSubcollection": False
}

class Policy:
    def __init__(self, assetId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################


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
