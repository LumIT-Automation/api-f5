from typing import Dict, Union

from f5.models.F5.PoolMember import PoolMember
from f5.models.F5.backend.Pool import Pool as Backend


MembersReference: Dict[str, Union[str, bool]] = {
    "link": "",
    "isSubcollection": False
}

class Pool:
    def __init__(self, assetId: int, partitionName: str, poolName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partition = partitionName
        self.name = poolName
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.allowNat: str = ""
        self.allowSnat: str = ""
        self.ignorePersistedWeight: str = ""
        self.ipTosToClient: str = ""
        self.ipTosToServer: str = ""
        self.linkQosToClient: str = ""
        self.linkQosToServer: str = ""
        self.loadBalancingMode: str = ""
        self.minActiveMembers: int = 0
        self.minUpMembers: int = 0
        self.minUpMembersAction: str = ""
        self.minUpMembersChecking: str = ""
        self.monitor: str = ""
        self.queueDepthLimit: int = 0
        self.queueOnConnectionLimit: str = ""
        self.queueTimeLimit: int = 0
        self.reselectTries: int = 0
        self.serviceDownAction: str = ""
        self.slowRampTime: int = 0
        self.membersReference: MembersReference = None



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self):
        try:
            i = Backend.info(self.assetId, self.partition, self.name)
            i["assetId"] = self.assetId

            return i
        except Exception as e:
            raise e



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



    def member(self, poolMemberName: str) -> PoolMember:
        try:
            return PoolMember(self.assetId, self.partition, self.name, poolMemberName)
        except Exception as e:
            raise e



    def members(self) -> dict:
        try:
            return PoolMember.list(self.assetId, self.partition, self.name) # return raw list.
        except Exception as e:
            raise e



    def addMember(self, data: dict) -> None:
        try:
            PoolMember.add(self.assetId, self.partition, self.name, data)
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
