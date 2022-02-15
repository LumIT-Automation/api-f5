from f5.models.F5.CertificateBase import CertificateBase


class Certificate(CertificateBase):
    def __init__(self, assetId: int, partitionName: str, name: str, *args, **kwargs):
        super().__init__(assetId, partitionName, "cert", name, *args, **kwargs)

        self.o = "cert"



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int) -> dict:
        try:
            return CertificateBase.list(assetId, "cert")
        except Exception as e:
            raise e



    @staticmethod
    def install(assetId: int, data: dict) -> None:
        try:
            CertificateBase.install(assetId, "cert", data)
        except Exception as e:
            raise e
