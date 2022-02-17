from f5.models.F5.backend.Certificate import Certificate as Backend


class CertificateBase:
    def __init__(self, assetId: int, partitionName: str, o: str, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partition = partitionName
        self.name = name

        self.o = o



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self):
        try:
            Backend.delete(self.assetId, self.partition, self.name, self.o)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, o: str) -> dict:
        try:
            return Backend.list(assetId, o)
        except Exception as e:
            raise e



    @staticmethod
    def install(assetId: int, o: str, data: dict) -> None:
        try:
            Backend.install(assetId, o, data)
        except Exception as e:
            raise e
