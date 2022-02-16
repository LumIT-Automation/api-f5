from typing import Dict, Union, Any

from f5.models.F5.CertificateBase import CertificateBase


ApiRawValues: Dict[str, str] = {
    "certificateKeySize": "",
    "expiration": "",
    "issuer": "",
    "publicKeyType": ""
}

CertValidatorsReference: Dict[str, Union[Any, bool]] = {
    "link": "",
    "isSubcollection": None
}

class Certificate(CertificateBase):
    def __init__(self, assetId: int, partitionName: str, name: str, *args, **kwargs):
        super().__init__(assetId, partitionName, "cert", name, *args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.name = name
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.apiRawValues: ApiRawValues = None
        self.city: str = ""
        self.commonName: str = ""
        self.country: str = ""
        self.emailAddress: str = ""
        self.fingerprint: str = ""
        self.organization: str = ""
        self.ou: str = ""
        self.state: str = ""
        self.certValidatorsReference: CertValidatorsReference = None



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
