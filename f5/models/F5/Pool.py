from f5.models.F5.PoolMember import PoolMember

from f5.models.F5.backend.Pool import Pool as Backend


class Pool:
    def __init__(self, assetId: int, partitionName: str, poolName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.poolName = poolName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self):
        try:
            return Backend.info(self.assetId, self.partitionName, self.poolName)
        except Exception as e:
            raise e



    def modify(self, data):
        try:
            Backend.modify(self.assetId, self.partitionName, self.poolName, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Backend.delete(self.assetId, self.partitionName, self.poolName)
        except Exception as e:
            raise e



    def member(self, poolMemberName: str) -> PoolMember:
        try:
            return PoolMember(self.assetId, self.partitionName, self.poolName, poolMemberName)
        except Exception as e:
            raise e



    def members(self) -> dict:
        try:
            return PoolMember.list(self.assetId, self.partitionName, self.poolName)
        except Exception as e:
            raise e



    def addMember(self, data: dict) -> None:
        try:
            PoolMember.add(self.assetId, self.partitionName, self.poolName, data)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str) -> dict:
        try:
            return Backend.list(assetId, partitionName)
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            Backend.add(assetId, data)
        except Exception as e:
            raise e
