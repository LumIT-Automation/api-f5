from f5.models.F5.repository.SnatPool import SnatPool as Repository


class SnatPool:
    def __init__(self, assetId: int, partitionName: str, snatPoolName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.snatPoolName = snatPoolName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, data):
        try:
            Repository.modify(self.assetId, self.partitionName, self.snatPoolName, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Repository.delete(self.assetId, self.partitionName, self.snatPoolName)
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
