from typing import List

from f5.models.F5.sys.backend.Folder import Folder as Backend

from f5.helpers.Misc import Misc


class Folder:
    def __init__(self, assetId: int, partitionName: str, folderName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partition: str = partitionName
        self.name: str = folderName
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.deviceGroup: str = ""
        self.hidden: bool = False
        self.inheritedDevicegroup: bool = False
        self.inheritedTrafficGroup: bool = False
        self.noRefCheck: bool = False
        self.trafficGroup: str = ""
        self.trafficGroupReference: str = ""



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, data):
        try:
            Backend.modify(self.assetId, self.partition, self.name, data)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Backend.delete(self.assetId, self.partition, self.name)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def dataList(assetId: int, partitionName: str) -> List[dict]:
        try:
            l = Backend.list(assetId, partitionName)
            for el in l:
                el["assetId"] = assetId

            return l
        except Exception as e:
            raise e




    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            Backend.add(assetId, data)
        except Exception as e:
            raise e
