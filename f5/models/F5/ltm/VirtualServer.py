from __future__ import annotations
from typing import List, Dict, Union

from f5.models.F5.ltm.Policy import Policy
from f5.models.F5.ltm.Profile import Profile
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
    def __init__(self, assetId: int, partitionName: str, virtualServerName: str, loadPolicies: bool = False, loadProfiles: bool = False, profileTypeFilter: list = None, *args, **kwargs):
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
        self.profiles: list = []
        profileTypeFilter = profileTypeFilter or []

        # Compositions.
        self.policies: List[Policy] = []


        self.__load(loadPolicies=loadPolicies, loadProfiles=loadProfiles, profileTypeFilter=profileTypeFilter)



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
    def list(assetId: int, partitionName: str, loadPolicies: bool = False, loadProfiles: bool = False) -> List[VirtualServer]:
        import threading
        l = []

        def loadVs(a, p, n, lpo, lpr, o):
            o.append(VirtualServer(a, p, n, lpo, lpr)) # append VirtualServer object.

        try:
            summary = Backend.list(assetId, partitionName)
            workers = [threading.Thread(target=loadVs, args=(assetId, partitionName, el.get("name", ""), loadPolicies, loadProfiles, l)) for el in summary]
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

    def __load(self, loadPolicies: bool = False, loadProfiles: bool = False, profileTypeFilter: list = None) -> None:
        profileTypeFilter = profileTypeFilter or []

        try:
            data = Backend.info(self.assetId, self.partition, self.name)
            if data:
                for k, v in data.items():
                    setattr(self, k, v)

                if loadPolicies:
                    for p in self.getPoliciesSummary():
                        # Append LTM Policy object.
                        self.policies.append(
                            Policy(self.assetId, p.get("partition", ""), p.get("subPath", ""), p.get("name", ""), loadRules=True)
                        )
                else:
                    del self.policies

                if loadProfiles:
                    self.profiles = self.getProfilesSummary() # List[Dict].
                    if profileTypeFilter:
                        profiles = []
                        for profileType in profileTypeFilter:
                            profileOfTypeList = Profile.list(assetId=self.assetId, partitionName=self.partition, profileType=profileType) # List[Profile]
                            # Keep only the profiles of the wanted types.
                            for profile in (p for p in self.profiles if p.get("fullPath", "") in [ pt.fullPath for pt in profileOfTypeList ] ):
                                profile.update({"type": profileType})
                                profiles.append(profile)
                        self.profiles = profiles
                else:
                    del self.profiles
            else:
                raise CustomException(status=404)
        except Exception as e:
            raise e
