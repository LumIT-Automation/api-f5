from typing import List

from f5.models.F5.Asset.repository.Asset import Asset as Repository
from f5.models.F5.Asset.repository.AssetAssetDr import AssetAssetDr as AssetDrRepository

from f5.helpers.Misc import Misc


class Asset:
    def __init__(self, assetId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(assetId)
        self.address: str = ""
        self.fqdn: str = ""
        self.baseurl: str = ""
        self.tlsverify: str = ""
        self.datacenter: str = ""
        self.environment: str = ""
        self.position: str = ""

        self.username: str = ""
        self.password: str = ""

        self.assetsDr: List[Asset] = []

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        o = dict()
        Misc.deepRepr(self, o)

        return o



    def modify(self, data: dict) -> None:
        try:
            Repository.modify(self.id, data)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository.delete(self.id)
            del self
        except Exception as e:
            raise e




    ####################################################################################################################
    # Public methods - disaster recovery relation
    ####################################################################################################################

    def drList(self) -> list:
        try:
            return AssetDrRepository.list(primaryAssetId=self.id)
        except Exception as e:
            raise e



    def drChange(self, drAssetId: int, enable: bool) -> None:
        try:
            AssetDrRepository.modify(primaryAssetId=self.id, drAssetId=drAssetId, enabled=enable)

        except Exception as e:
            raise e



    def drRemove(self, drAssetId: int) -> None:
        try:
            AssetDrRepository.delete(primaryAssetId=self.id, drAssetId=drAssetId)

        except Exception as e:
            raise e



    def drAdd(self, drAssetId: int, enabled: bool) -> None:
        try:
            AssetDrRepository.add(primaryAssetId=self.id, drAssetId=drAssetId, enabled=enabled)

        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def dataList() -> list:
        try:
            return Repository.list()
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> None:
        from f5.models.Permission.Partition import Partition as PermissionPartition

        try:
            aId = Repository.add(data)

            # When inserting an asset, add the "any" partition (Permission).
            PermissionPartition.add(aId, "any")
        except Exception as e:
            raise e



    @staticmethod
    def purgeAll() -> None:
        from f5.models.Permission.Partition import Partition

        try:
            Partition.purgeAll()
            Repository.purgeAll()
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            data = Repository.get(self.id)
            for k, v in data.items():
                setattr(self, k, v)

            # Load related disaster recovery assets.
            for dr in AssetDrRepository.list(primaryAssetId=self.id):
                self.assetsDr.append(
                    Asset(dr["id"])
                )
        except Exception as e:
            raise e
