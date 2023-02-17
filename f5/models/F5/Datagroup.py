from typing import Dict

from f5.models.F5.backend.Datagroup import Datagroup as Backend


Records: Dict[str, str] = {
    "name": "",
    "data": ""
}

class Datagroup:
    def __init__(self, assetId: int, partitionName: str, datagroupType: str, datagroupName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.partition: str = partitionName
        self.type: str = datagroupType
        self.name: str = datagroupName
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.records: Records = None



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, data):
        try:
            Backend.modify(self.assetId, self.partition, self.type, self.name, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Backend.delete(self.assetId, self.partition, self.type, self.name)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def types(assetId: int, partitionName: str) -> list:
        try:
            return Backend.types(assetId, partitionName)
        except Exception as e:
            raise e



    @staticmethod
    def list(assetId: int, partitionName: str, datagroupType: str) -> dict:
        try:
            l = Backend.list(assetId, partitionName, datagroupType)
            for el in l:
                el["assetId"] = assetId

            return l
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, datagroupType: str, data: dict) -> None:
        try:
            Backend.add(assetId, datagroupType, data)
        except Exception as e:
            raise e
