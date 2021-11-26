from f5.models.F5.Partition import Partition as F5Partition

from f5.repository.Partition import Partition as Repository


class Partition:
    def __init__(self, id: int, partitionName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id
        self.partition = partitionName
        self.description = ""



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def exists(self) -> bool:
        try:
            pid = self.info()["id"] # just a probe.
            return True
        except Exception:
            return False



    def info(self) -> dict:
        try:
            return Repository.get(self.id, self.partition)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository.delete(self.id, self.partition)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def add(id, partition) -> int:
        if partition == "any":
            try:
                pid = Repository.add(id, partition)
                return pid
            except Exception as e:
                raise e

        else:
            # Check if assetId/partition is a valid F5 partition (at the time of the insert).
            partitions = F5Partition.list(id)["data"]["items"]

            for v in partitions:
                if v["partition"] == partition:
                    try:
                        pid = Repository.add(id, partition)
                        return pid
                    except Exception as e:
                        raise e
