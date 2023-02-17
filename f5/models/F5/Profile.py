from typing import Dict

from f5.models.F5.backend.Profile import Profile as Backend

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



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    @staticmethod
    def types(assetId: int, partitionName: str) -> list:
        try:
            return Backend.types(assetId, partitionName)
        except Exception as e:
            raise e



    def info(self, silent: bool = False):
        try:
            i = Backend.info(self.assetId, self.type, self.partition, self.name, silent)

            i["assetId"] = self.assetId
            i["type"] = self.type

            return i
        except Exception as e:
            raise e



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
    def list(assetId: int, partitionName: str, profileType: str) -> dict:
        try:
            l = Backend.list(assetId, partitionName, profileType)
            for el in l:
                el["assetId"] = assetId
                el["type"] = profileType

            return l
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, profileType: str, data: dict) -> None:
        try:
            Backend.add(assetId, profileType, data)
        except Exception as e:
            raise e
