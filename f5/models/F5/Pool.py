import json

from f5.models.F5.Asset.Asset import Asset
from f5.models.F5.PoolMember import PoolMember

from f5.helpers.ApiSupplicant import ApiSupplicant


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
        o = dict()

        try:
            f5 = Asset(self.assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+self.partitionName+"~"+self.poolName+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            o["data"] = api.get()
        except Exception as e:
            raise e

        return o



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



    def modify(self, data):
        try:
            f5 = Asset(self.assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+self.partitionName+"~"+self.poolName+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.patch(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps(data)
            )
        except Exception as e:
            raise e



    def addMember(self, data: dict) -> None:
        try:
            PoolMember.add(self.assetId, self.partitionName, self.poolName, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            f5 = Asset(self.assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+self.partitionName+"~"+self.poolName+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.delete(
                additionalHeaders={
                    "Content-Type": "application/json",
                }
            )
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str) -> dict:
        o = dict()

        try:
            f5 = Asset(assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/?$filter=partition+eq+"+partitionName,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            o["data"] = api.get()
        except Exception as e:
            raise e

        return o



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.post(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps(data)
            )
        except Exception as e:
            raise e
