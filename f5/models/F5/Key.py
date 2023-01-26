from typing import List

from f5.models.F5.CertificateKeyBase import CertificateKeyBase as KeyBase


class Key(KeyBase):
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
    # Public methods
    ####################################################################################################################

    def update(self, data: dict) -> None:
        try:
            KeyBase(self.assetId, self.partition, "key", self.name).modifyObject(data)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str) -> List[dict]:
        try:
            return Key.listObjects(assetId, partitionName, "key")
        except Exception as e:
            raise e



    @staticmethod
    def install(assetId: int, partitionName: str, data: dict) -> None:
        try:
            Key.installObject(assetId, partitionName, "key", data)
        except Exception as e:
            raise e
