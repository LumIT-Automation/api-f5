from typing import List, Dict, Union

from f5.models.F5.ltm.backend.VirtualServer import VirtualServer as Backend

from f5.helpers.Exception import CustomException
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
    def __init__(self, assetId: int, partitionName: str, virtualServerName: str, loadPolicies: bool = False, loadProfiles: bool = False, *args, **kwargs):
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

        self.policies: List[dict] = []
        self.profiles: List[dict] = []

        self.__load(loadPolicies=loadPolicies, loadProfiles=loadProfiles)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        return Misc.deepRepr(self)



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



    def getPoliciesSummary(self) -> List[dict]:
        try:
            return Backend.policies(self.assetId, self.partition, self.name)
        except Exception as e:
            raise e



    def getProfilesSummary(self) -> List[dict]:
        try:
            return Backend.profiles(self.assetId, self.partition, self.name)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def dataList(assetId: int, partitionName: str, loadPolicies: bool = False, loadProfiles: bool = False) -> List[Dict]:
        import threading

        def loadData(a, p, n, o):
            o["assetId"] = assetId

            if loadPolicies:
                o["policies"] = Backend.policies(a, p, n)
            if loadProfiles:
                o["profiles"] = Backend.profiles(a, p, n)

        try:
            l = Backend.list(assetId, partitionName)
            workers = [threading.Thread(target=loadData, args=(assetId, partitionName, el.get("name", ""), el)) for el in l]
            for w in workers:
                w.start()
            for w in workers:
                w.join()

            return l
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            Backend.add(assetId, data)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self, loadPolicies: bool = False, loadProfiles: bool = False) -> None:
        try:
            data = Backend.info(self.assetId, self.partition, self.name)
            if data:
                if loadPolicies:
                    data["policies"] = self.getPoliciesSummary()
                if loadProfiles:
                    data["profiles"] = self.getProfilesSummary()

                for k, v in data.items():
                    setattr(self, k, v)
            else:
                raise CustomException(status=404)
        except Exception as e:
            raise e
