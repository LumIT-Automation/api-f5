from typing import List, Dict, Union

from f5.models.F5.backend.VirtualServer import VirtualServer as Backend

from f5.helpers.Misc import Misc


SourceAddressTranslation: Dict[str, str] = {
    "type": "",
    "pool": ""
}

PoolReference: Dict[str, str] = {
    "link": ""
}

Reference: Dict[str, Union[str, bool]] = {
    "link": "",
    "isSubcollection": False
}

class VirtualServer:
    def __init__(self, assetId: int, partitionName: str, virtualServerName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partition = partitionName
        self.name = virtualServerName
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.addressStatus: str = ""
        self.autoLasthop: str = ""
        self.cmpEnabled: str = ""
        self.connectionLimit: int = 0
        self.creationTime: str = ""
        self.destination: str = ""
        self.enabled: bool = False
        self.evictionProtected: str = ""
        self.gtmScore: int = 0
        self.ipProtocol: str = ""
        self.lastModifiedTime: str = ""
        self.mask: str = ""
        self.mirror: str = ""
        self.mobileAppTunnel: str = ""
        self.nat64: str = ""
        self.pool: str = ""
        self.serversslUseSni: str = ""
        self.poolReference: PoolReference = None
        self.rateLimit: str = ""
        self.rateLimitDstMask: int = 0
        self.rateLimitMode: str = ""
        self.rateLimitSrcMask: int = 0
        self.serviceDownImmediateAction: str = ""
        self.source: str = ""
        self.sourceAddressTranslation: SourceAddressTranslation = None
        self.sourcePort: str = ""
        self.synCookieStatus: str = ""
        self.translateAddress: str = ""
        self.translatePort: str = ""
        self.vlansDisabled: bool = False
        self.vsIndex: int = 0
        self.policiesReference: Reference = None
        self.profilesReference: Reference = None
        self.rules: list = []
        self.rulesReference: Reference = None



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



    def policies(self):
        try:
            return Backend.policies(self.assetId, self.partition, self.name)
        except Exception as e:
            raise e



    def profiles(self):
        try:
            return Backend.profiles(self.assetId, self.partition, self.name)
        except Exception as e:
            raise e



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
    def list(assetId: int, partitionName: str) -> List[Dict]:
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
