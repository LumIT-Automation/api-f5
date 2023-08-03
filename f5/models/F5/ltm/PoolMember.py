from typing import Dict

from f5.models.F5.ltm.backend.PoolMember import PoolMember as Backend

from f5.helpers.Misc import Misc


Fqdn: Dict[str, str] = {
    "autopopulate": ""
}

class PoolMember:
    def __init__(self, assetId: int, poolName: str, partition: str, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.partition: str = partition
        self.poolName: str = poolName
        self.name: str = name
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.address: str = ""
        self.connectionLimit: int = 0
        self.dynamicRatio: int = 0
        self.ephemeral: bool
        self.inheritProfile: str = ""
        self.logging: str = ""
        self.monitor: str = ""
        self.priorityGroup: int = 0
        self.rateLimit: str = ""
        self.ratio: int = 0
        self.session: str = ""
        self.state: str = ""
        self.fqdn: Fqdn
        self.enabledState: str = ""



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            i = Backend.info(self.assetId, self.partition, self.poolName, self.name)
            i["assetId"] = self.assetId

            return i
        except Exception as e:
            raise e



    def stats(self) -> dict:
        try:
            return Backend.stats(self.assetId, self.partition, self.poolName, self.name)
        except Exception as e:
            raise e



    def modify(self, data: dict) -> None:
        try:
            Backend.modify(self.assetId, self.partition, self.poolName, self.name, data)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Backend.delete(self.assetId, self.partition, self.poolName, self.name)
            del self
        except Exception as e:
            raise e


    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str, poolName: str) -> dict:
        try:
            l = Backend.list(assetId, partitionName, poolName)
            for el in l:
                el["assetId"] = assetId

            return l
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, partitionName: str, poolName: str, data: dict) -> None:
        try:
            Backend.add(assetId, partitionName, poolName, data)
        except Exception as e:
            raise e
