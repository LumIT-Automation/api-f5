from f5.models.F5.repository.VirtualServer import VirtualServer as Repository


class VirtualServer:
    def __init__(self, assetId: int, partitionName: str, virtualServerName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.virtualServerName = virtualServerName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self):
        try:
            return Repository.info(self.assetId, self.partitionName, self.virtualServerName)
        except Exception as e:
            raise e



    def policies(self):
        try:
            return Repository.policies(self.assetId, self.partitionName, self.virtualServerName)
        except Exception as e:
            raise e



    def profiles(self):
        try:
            return Repository.profiles(self.assetId, self.partitionName, self.virtualServerName)
        except Exception as e:
            raise e



    def modify(self, data):
        try:
            Repository.modify(self.assetId, self.partitionName, self.virtualServerName, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Repository.delete(self.assetId, self.partitionName, self.virtualServerName)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str) -> dict:
        try:
            return Repository.list(assetId, partitionName)
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            Repository.add(assetId, data)
        except Exception as e:
            raise e
