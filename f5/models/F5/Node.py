from f5.models.F5.repository.Node import Node as Repository


class Node:
    def __init__(self, assetId: int, partitionName: str, nodeName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.nodeName = nodeName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, data):
        try:
            Repository.modify(self.assetId, self.partitionName, self.nodeName, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Repository.delete(self.assetId, self.partitionName, self.nodeName)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str, silent: bool = False) -> dict:
        try:
            return Repository.list(assetId, partitionName, silent)
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            Repository.add(assetId, data)
        except Exception as e:
            raise e



    @staticmethod
    def getNameFromAddress(assetId: int, partitionName: str, address: str, silent: bool = False) -> str:
        name = ""
        try:
            data = Node.list(assetId, partitionName, silent=silent)
            for nel in data["items"]:
                if nel["address"] == address:
                    name = nel["name"]

            return name
        except Exception as e:
            raise e
