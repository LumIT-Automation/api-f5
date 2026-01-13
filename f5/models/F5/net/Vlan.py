from typing import List, Dict

from f5.models.F5.net.backend.Vlan import Vlan as Backend


VlansReference: Dict[str, str] = {
    "link": ""
}

class Vlan:
    def __init__(self, assetId: int, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.name: str = name
        self.id: int = 0
        self.partition: str = ""
        self.fullPath: str = ""
        self.generation: int = 0
        self.connectionLimit: int = 0
        self.selfLink: str = ""

        self.strict: str = ""
        self.throughputCapacity: str = ""
        self.vlans: List[str] = []
        self.vlansReference: List[VlansReference] = []



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            i = Backend.info(self.assetId, self.name)
            i["assetId"] = self.assetId

            return i
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def dataList(assetId: int) -> list:
        try:
            l = Backend.list(assetId)
            for el in l:
                el["assetId"] = assetId

            return l
        except Exception as e:
            raise e
