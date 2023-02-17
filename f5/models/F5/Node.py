from typing import Dict, Union

from f5.models.F5.backend.Node import Node as Backend

from f5.helpers.Misc import Misc


Fqdn: Dict[str, Union[str, int]] = {
    "addressFamily": "",
    "autopopulate": "",
    "interval": "",
    "downInterval": 0
}

class Node:
    def __init__(self, assetId: int, partitionName: str, nodeName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partition: str = partitionName
        self.name: str = nodeName
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.address: str = ""
        self.connectionLimit: int = 0
        self.dynamicRatio: int = 0
        self.ephemeral: bool
        self.fqdn = Fqdn
        self.logging: str = ""
        self.monitor: str = ""
        self.rateLimit: str = ""
        self.ratio: int = 0
        self.session: str = ""
        self.state: str = ""



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, data):
        try:
            Backend.modify(self.assetId, self.partition, self.name, data)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Backend.delete(self.assetId, self.partition, self.name)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str, silent: bool = False) -> dict:
        try:
            l = Backend.list(assetId, partitionName, silent)
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



    @staticmethod
    def getNameFromAddress(assetId: int, partitionName: str, address: str, silent: bool = False) -> str:
        name = ""

        try:
            data = Node.list(assetId, partitionName, silent=silent)
            for nel in data:
                if nel["address"] == address:
                    name = nel["name"]

            return name
        except Exception as e:
            raise e
