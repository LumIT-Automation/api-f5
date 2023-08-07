from __future__ import annotations
from typing import Dict, List

from f5.models.F5.ltm.backend.Profile import Profile as Backend

from f5.helpers.Exception import CustomException
from f5.helpers.Misc import Misc


Link: Dict[str, str] = {
    "link": ""
}

class Profile:
    def __init__(self, assetId: int, partitionName: str, profileType: str, profileName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.partition: str = partitionName
        self.type: str = profileType
        self.name: str = profileName
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.defaultsFrom: str = ""
        self.defaultsFromReference: Link = None
        self.clientTimeout: int = 0
        self.ipTtlV4: int = 0
        self.ipTtlV6: int = 0
        self.mssOverride: int = 0
        self.otherPvaClientpktsThreshold: int = 0
        self.otherPvaServerpktsThreshold: int = 0
        self.pvaDynamicClientPackets: int = 0
        self.pvaDynamicServerPackets: int = 0
        self.receiveWindowSize: int = 0
        self.synCookieMss: int = 0
        self.tcpTimeWaitTimeout: int = 0
        self.appService: str = ""
        self.description: str = ""
        self.explicitFlowMigration: str = ""
        self.hardwareSynCookie: str = ""
        self.idleTimeout: str = ""
        self.ipDfMode: str = ""
        self.ipTosToClient: str = ""
        self.ipTosToServer: str = ""
        self.ipTtlMode: str = ""
        self.keepAliveInterval: str = ""
        self.lateBinding: str = ""
        self.linkQosToClient: str = ""
        self.linkQosToServer: str = ""
        self.looseClose: str = ""
        self.looseInitialization: str = ""
        self.otherPvaOffloadDirection: str = ""
        self.otherPvaWhentoOffload: str = ""
        self.priorityToClient: str = ""
        self.priorityToServer: str = ""
        self.pvaAcceleration: str = ""
        self.pvaFlowAging: str = ""
        self.pvaFlowEvict: str = ""
        self.pvaOffloadDynamic: str = ""
        self.pvaOffloadState: str = ""
        self.reassembleFragments: str = ""
        self.resetOnTimeout: str = ""
        self.rttFromClient: str = ""
        self.rttFromServer: str = ""
        self.serverSack: str = ""
        self.serverTimestamp: str = ""
        self.softwareSynCookie: str = ""
        self.synCookieEnable: str = ""
        self.synCookieWhitelist: str = ""
        self.tcpCloseTimeout: str = ""
        self.tcpGenerateIsn: str = ""
        self.tcpHandshakeTimeout: str = ""
        self.tcpPvaWhentoOffload: str = ""
        self.tcpStripSack: str = ""
        self.tcpWscaleMode: str = ""
        self.tcpTimestampMode: str = ""
        self.timeoutRecovery: str = ""
        self.cert: str = ""
        self.key: str = ""

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        return Misc.deepRepr(self)



    def modify(self, data):
        try:
            Backend.modify(self.assetId, self.type, self.partition, self.name, data)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Backend.delete(self.assetId, self.type, self.partition, self.name)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def types(assetId: int, partitionName: str) -> list:
        try:
            return Backend.types(assetId, partitionName)
        except Exception as e:
            raise e



    @staticmethod
    def list(assetId: int, partitionName: str, profileType: str) -> List[Profile]:
        import threading
        l = []

        def loadProfile(a, p, t, n, o):
            o.append(Profile(a, p, t, n)) # append Profile object.

        try:
            summary = Backend.list(assetId, partitionName, profileType)
            workers = [threading.Thread(target=loadProfile, args=(assetId, partitionName, profileType, el.get("name", ""), l)) for el in summary]
            for w in workers:
                w.start()
            for w in workers:
                w.join()

            return l
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, profileType: str, data: dict) -> None:
        try:
            Backend.add(assetId, profileType, data)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            data = Backend.info(self.assetId, self.type, self.partition, self.name)
            if data:
                for k, v in data.items():
                    setattr(self, k, v)
            else:
                raise CustomException(status=404)
        except Exception as e:
            raise e
