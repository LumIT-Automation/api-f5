from typing import List, Dict

from f5.models.F5.net.backend.RouteDomain import RouteDomain as Backend


VlansReference: Dict[str, str] = {
    "link": ""
}

class RouteDomain:
    def __init__(self, assetId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.name: str = ""
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
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def dataList(assetId: int) -> dict:
        try:
            l = Backend.list(assetId)
            for el in l:
                el["assetId"] = assetId

            return l
        except Exception as e:
            raise e
