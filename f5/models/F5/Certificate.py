from f5.models.F5.backend.Certificate import Certificate as Backend


class Certificate:
    def __init__(self, assetId: int, partitionName: str, resourceName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.resourceName = resourceName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self, what):
        if any(w in what for w in ("cert", "key")):
            try:
                Backend.delete(self.assetId, self.partitionName, self.resourceName, what)
            except Exception as e:
                raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, what: str) -> dict:
        o = dict()

        if any(w in what for w in ("cert", "key")):
            try:
                return Backend.list(assetId, what)
            except Exception as e:
                raise e

        return o



    @staticmethod
    def install(assetId: int, what: str, data: dict) -> None:
        if any(w in what for w in ("cert", "key")):
            try:
                Backend.install(assetId, what, data)
            except Exception as e:
                raise e
