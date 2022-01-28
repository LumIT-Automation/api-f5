from f5.models.F5.repository.Monitor import Monitor as Repository


class Monitor:
    def __init__(self, assetId: int, partitionName: str, monitorType: str, monitorName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.monitorType = monitorType
        self.monitorName = monitorName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self, silent: bool = False):
        try:
            return Repository.info(self.assetId, self.partitionName, self.monitorType, self.monitorName, silent)
        except Exception as e:
            raise e



    def modify(self, data):
        try:
            Repository.modify(self.assetId, self.partitionName, self.monitorType, self.monitorName, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Repository.delete(self.assetId, self.partitionName, self.monitorType, self.monitorName)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def types(assetId: int, partitionName: str) -> dict:
        o = dict()

        try:
            o["items"] = Repository.types(assetId, partitionName)
        except Exception as e:
            raise e

        return o



    @staticmethod
    def list(assetId: int, partitionName: str, monitorType: str) -> dict:
        try:
            return Repository.list(assetId, partitionName, monitorType)
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, monitorType: str, data: dict) -> None:
        try:
            Repository.add(assetId, monitorType, data)
        except Exception as e:
            raise e
