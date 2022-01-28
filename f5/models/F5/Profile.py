from f5.models.F5.backend.Profile import Profile as Backend


class Profile:
    def __init__(self, assetId: int, partitionName: str, profileType: str, profileName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.profileType = profileType
        self.profileName = profileName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    @staticmethod
    def types(assetId: int, partitionName: str) -> dict:
        o = dict()

        try:
            items = Backend.types(assetId, partitionName)
            o["items"] = items
        except Exception as e:
            raise e

        return o



    def info(self, silent: bool = False):
        try:
            return Backend.info(self.assetId, self.profileType, self.partitionName, self.profileName, silent)
        except Exception as e:
            raise e



    def modify(self, data):
        try:
            Backend.modify(self.assetId, self.profileType, self.partitionName, self.profileName, data)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Backend.delete(self.assetId, self.profileType, self.partitionName, self.profileName)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str, profileType: str) -> dict:
        try:
            return Backend.list(assetId, partitionName, profileType)
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, profileType: str, data: dict) -> None:
        try:
            Backend.add(assetId, profileType, data)
        except Exception as e:
            raise e
