from f5.models.F5.backend.Monitor import Monitor as Backend


class Monitor:
    def __init__(self, assetId: int, partitionName: str, monitorType: str, monitorName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.partition: str = partitionName
        self.type: str = monitorType
        self.name: str = monitorName
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.defaultsFrom: str = ""
        self.destination: str = ""
        self.interval: str = ""
        self.manualResume: str = ""
        self.timeUntilUp: int = 0
        self.timeout: int = 0
        self.transparent: str = ""
        self.upInterval: int = 0



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self, silent: bool = False):
        try:
            i = Backend.info(self.assetId, self.partition, self.type, self.name, silent)

            i["assetId"] = self.assetId
            i["type"] = self.type

            return i
        except Exception as e:
            raise e



    def modify(self, data):
        try:
            Backend.modify(self.assetId, self.partition, self.type, self.name, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Backend.delete(self.assetId, self.partition, self.type, self.name)
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
    def list(assetId: int, partitionName: str, monitorType: str) -> dict:
        try:
            l = Backend.list(assetId, partitionName, monitorType)
            for el in l:
                el["assetId"] = assetId
                el["type"] = monitorType

            return l
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, monitorType: str, data: dict) -> None:
        try:
            Backend.add(assetId, monitorType, data)
        except Exception as e:
            raise e
