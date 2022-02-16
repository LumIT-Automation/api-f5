from f5.models.F5.CertificateBase import CertificateBase


class Key(CertificateBase):
    def __init__(self, assetId: int, partitionName: str, name: str, *args, **kwargs):
        super().__init__(assetId, partitionName, "key", name, *args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.name = name



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int) -> dict:
        try:
            return CertificateBase.list(assetId, "key")
        except Exception as e:
            raise e



    @staticmethod
    def install(assetId: int, data: dict) -> None:
        try:
            CertificateBase.install(assetId, "key", data)
        except Exception as e:
            raise e
