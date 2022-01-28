from f5.models.F5.repository.Certificate import Certificate as Repository


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
                Repository.delete(self.assetId, self.partitionName, self.resourceName, what)
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
                return Repository.list(assetId, what)
            except Exception as e:
                raise e

        return o



    @staticmethod
    def install(assetId: int, what: str, data: dict) -> None:
        if any(w in what for w in ("cert", "key")):
            try:
                Repository.install(assetId, what, data)
            except Exception as e:
                raise e
