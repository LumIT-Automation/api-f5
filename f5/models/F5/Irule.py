from f5.models.F5.repository.Irule import Irule as Repository


class Irule:
    def __init__(self, assetId: int, partitionName: str, iruleName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.iruleName = iruleName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, data):
        try:
            Repository.modify(self.assetId, self.partitionName, self.iruleName, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Repository.delete(self.assetId, self.partitionName, self.iruleName)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str) -> dict:
        try:
            return Repository.list(assetId, partitionName)
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            Repository.add(assetId, data)
        except Exception as e:
            raise e
