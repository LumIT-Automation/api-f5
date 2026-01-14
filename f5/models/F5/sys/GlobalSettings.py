from typing import List, Dict

from f5.models.F5.sys.backend.GlobalSettings import GlobalSettings as Backend


SelfsReference: Dict[str, str] = {
    "link": ""
}

class GlobalSettings:
    def __init__(self, assetId: int, name: str, *args, **kwargs):
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



    ####################################################################################################################
    # Public methods
    ####################################################################################################################
    @staticmethod
    def info(assetId: int) -> dict:
        try:
            i = Backend.info(assetId)
            i["assetId"] = assetId

            return i
        except Exception as e:
            raise e


