from typing import List
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

    def delete(self) -> None:
        try:
            Backend.delete(self.assetId, self.partition, self.name, self.o)
        except Exception as e:
            raise e



    def modifyObject(self, data: dict) -> None:
        try:
            Backend.update(self.assetId, self.partition, self.name, self.o, data)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listObjects(assetId: int, partitionName: str, o: str) -> List[dict]:
        try:
            l = Backend.list(assetId, partitionName, o)
            for el in l:
                el["assetId"] = assetId
                el["partition"] = partitionName
                el["content_base64"] = "[undisclosed]"

            return l
        except Exception as e:
            raise e



    @staticmethod
    def installObject(assetId: int, partitionName: str, o: str, data: dict) -> None:
        try:
            Backend.install(assetId, partitionName, o, data)
        except Exception as e:
            raise e
