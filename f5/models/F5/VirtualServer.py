from f5.models.F5.backend.VirtualServer import VirtualServer as Backend


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
            return Backend.info(self.assetId, self.partitionName, self.virtualServerName)
        except Exception as e:
            raise e



    def policies(self):
        try:
            return Backend.policies(self.assetId, self.partitionName, self.virtualServerName)
        except Exception as e:
            raise e



    def profiles(self):
        try:
            return Backend.profiles(self.assetId, self.partitionName, self.virtualServerName)
        except Exception as e:
            raise e



    def modify(self, data):
        try:
            Backend.modify(self.assetId, self.partitionName, self.virtualServerName, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Backend.delete(self.assetId, self.partitionName, self.virtualServerName)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str) -> dict:
        try:
            return Backend.list(assetId, partitionName)
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            Backend.add(assetId, data)
        except Exception as e:
            raise e
