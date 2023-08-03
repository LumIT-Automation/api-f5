from typing import List, Dict, Union

from f5.models.F5.sys.CertificateKeyBase import CertificateKeyBase as CertificateBase


ApiRawValues: Dict[str, str] = {
    "certificateKeySize": "",
    "expiration": "",
    "issuer": "",
    "publicKeyType": ""
}

CertValidatorsReference: Dict[str, Union[str, bool]] = {
    "link": "",
    "isSubcollection": False
}

class Certificate(CertificateBase):
    def __init__(self, assetId: int, partitionName: str, name: str, *args, **kwargs):
        super().__init__(assetId, partitionName, "cert", name, *args, **kwargs)

        self.assetId: int = int(assetId)
        self.partition: str = partitionName
        self.name: str = name
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
    # Public methods
    ####################################################################################################################

    def update(self, data: dict) -> None:
        try:
            CertificateBase(self.assetId, self.partition, "cert", self.name).modifyObject(data)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def dataList(assetId: int, partitionName: str) -> List[dict]:
        try:
            return Certificate.listObjects(assetId, partitionName, "cert")
        except Exception as e:
            raise e



    @staticmethod
    def install(assetId: int, partitionName: str, data: dict) -> None:
        try:
            Certificate.installObject(assetId, partitionName, "cert", data)
        except Exception as e:
            raise e
