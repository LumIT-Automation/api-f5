from f5.models.F5.Partition import Partition as F5Partition

from f5.models.Permission.repository.Partition import Partition as Repository


class Partition:
    def __init__(self, id: int = 0, assetId: int = 0, name: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.id_asset: int = int(assetId)
        self.partition: str = name
        self.description: str = ""

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self) -> None:
        try:
            Repository.delete(self.id)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def add(assetId: int, partition: str, role: str = "") -> int:
        # If admin: "any" is the only valid choice (on selected assetId).
        if role == "admin":
            partition = "any"

        if partition == "any":
            try:
                did = Repository.add(assetId, partition)
                return did
            except Exception as e:
                raise e

        else:
            # Check if assetId/partition is a valid F5 partition (at the time of the insert).
            partitions = F5Partition.list(assetId)
            for v in partitions:
                if v["name"] == partition:
                    try:
                        pid = Repository.add(assetId, partition)
                        return pid
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
