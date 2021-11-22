from f5.models.F5.Partition import Partition as F5Partition

from f5.repository.Partition import Partition as Repository



class Partition:
    def __init__(self, assetId: int, partitionId: int = 0, partitionName: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = assetId
        self.partitionId = id
        self.partitionName = partitionName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def exists(self) -> bool:
        try:
            pid = self.info()["id"]
            return True
        except Exception:
            return False



    def info(self) -> dict:
        try:
            return Repository(self.assetId, partitionName=self.partitionName).info()
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository(self.assetId, partitionName=self.partitionName).delete()
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def add(assetId, partitionName) -> int:
        if partitionName == "any":
            try:
                pid = Repository.add(assetId, partitionName)
                return pid
            except Exception as e:
                raise e

        else:
            # Check if assetId/partitionName is a valid F5 partition (at the time of the insert).
            partitions = F5Partition.list(assetId)["data"]["items"]

            for v in partitions:
                if v["name"] == partitionName:
                    try:
                        pid = Repository.add(assetId, partitionName)
                        return pid
                    except Exception as e:
                        raise e
