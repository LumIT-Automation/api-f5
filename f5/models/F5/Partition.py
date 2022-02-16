from f5.models.F5.backend.Partition import Partition as Backend


class Partition:
    def __init__(self, assetId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.name: str = ""
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.defaultRouteDomain: int = 0



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int) -> dict:
        try:
            l = Backend.list(assetId)
            for el in l:
                el["assetId"] = assetId
            return l
        except Exception as e:
            raise e
