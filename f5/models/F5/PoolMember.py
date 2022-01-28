from f5.models.F5.repository.PoolMember import PoolMember as Repository


class PoolMember:
    def __init__(self, assetId: int, poolName: str, partition: str, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partition = str(partition)
        self.poolName = str(poolName)
        self.name = str(name)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return Repository.info(self.assetId, self.partition, self.poolName, self.name)
        except Exception as e:
            raise e



    def stats(self) -> dict:
        try:
            return Repository.stats(self.assetId, self.partition, self.poolName, self.name)
        except Exception as e:
            raise e



    def modify(self, data: dict) -> None:
        try:
            Repository.modify(self.assetId, self.partition, self.poolName, self.name, data)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository.delete(self.assetId, self.partition, self.poolName, self.name)
        except Exception as e:
            raise e


    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str, poolName: str) -> dict:
        try:
            return Repository.list(assetId, partitionName, poolName)
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, partitionName: str, poolName: str, data: dict) -> None:
        try:
            Repository.add(assetId, partitionName, poolName, data)
        except Exception as e:
            raise e
