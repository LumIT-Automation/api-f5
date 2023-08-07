from f5.models.F5.auth.Partition import Partition as F5Partition

from f5.models.Permission.repository.Partition import Partition as Repository


class Partition:
    def __init__(self, id: int = 0, assetId: int = 0, name: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.id_asset: int = int(assetId) # simple property, not composition.
        self.partition: str = name
        self.description: str = ""

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self) -> None:
        try:
            Repository.delete(self.id)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def add(asset: int, partition: str) -> int:
        if partition == "any":
            try:
                return Repository.add(asset, partition)
            except Exception as e:
                raise e
        else:
            # Check if assetId/partition is a valid F5 partition (at the time of the insert).
            partitions = F5Partition.dataList(asset)
            for v in partitions:
                if v["name"] == partition:
                    try:
                        return Repository.add(asset, partition)
                    except Exception as e:
                        raise e



    @staticmethod
    def purgeAll() -> None:
        try:
            Repository.purgeAll()
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository.get(self.id, self.id_asset, self.partition)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
