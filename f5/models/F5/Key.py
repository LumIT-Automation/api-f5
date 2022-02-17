from f5.models.F5.CertificateBase import CertificateBase


class Key(CertificateBase):
    def __init__(self, assetId: int, partitionName: str, name: str, *args, **kwargs):
        super().__init__(assetId, partitionName, "key", name, *args, **kwargs)

        self.assetId: int = int(assetId)
        self.partition: str = partitionName
        self.name: str = name
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.keySize: int = 0
        self.keyType: str = ""
        self.securityType: str = ""



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int) -> dict:
        try:
            l = CertificateBase.list(assetId, "key")
            for el in l:
                el["assetId"] = assetId

            return l
        except Exception as e:
            raise e



    @staticmethod
    def install(assetId: int, data: dict) -> None:
        try:
            CertificateBase.install(assetId, "key", data)
        except Exception as e:
            raise e
