from typing import List, Dict

from f5.models.F5.backend.SnatPool import SnatPool as Backend


MembersReference: Dict[str, str] = {
    "link": ""
}

class SnatPool:
    def __init__(self, assetId: int, partitionName: str, snatPoolName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.partition: str = partitionName
        self.name: str = snatPoolName
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.members: List[str]
        self.membersReference: MembersReference = None



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, data):
        try:
            Backend.modify(self.assetId, self.partition, self.name, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Backend.delete(self.assetId, self.partition, self.name)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str) -> dict:
        try:
            l = Backend.list(assetId, partitionName)
            for el in l:
                el["assetId"] = assetId

            return l
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            Backend.add(assetId, data)
        except Exception as e:
            raise e
