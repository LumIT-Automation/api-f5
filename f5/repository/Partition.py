from django.db import connection

from f5.models.F5.Partition import Partition as F5Partition

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Partition:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(assetId: int, partitionName: str) -> dict:
        c = connection.cursor()

        try:
            c.execute("SELECT * FROM `partition` WHERE `partition` = %s AND id_asset = %s", [
                partitionName,
                assetId
            ])

            return DBHelper.asDict(c)[0]
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def delete(assetId: int, partitionName: str) -> None:
        c = connection.cursor()

        try:
            c.execute("DELETE FROM `partition` WHERE `partition` = %s AND id_asset = %s", [
                partitionName,
                assetId
            ])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(assetId, partitionName) -> int:
        c = connection.cursor()

        if partitionName == "any":
            try:
                c.execute("INSERT INTO `partition` (id_asset, `partition`) VALUES (%s, %s)", [
                    assetId,
                    partitionName
                ])

                return c.lastrowid
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        else:
            # Check if assetId/partitionName is a valid F5 partition (at the time of the insert).
            f5Partitions = F5Partition.list(assetId)["data"]["items"]

            for v in f5Partitions:
                if v["name"] == partitionName:
                    try:
                        c.execute("INSERT INTO `partition` (id_asset, `partition`) VALUES (%s, %s)", [
                            assetId,
                            partitionName
                        ])

                        return c.lastrowid
                    except Exception as e:
                        raise CustomException(status=400, payload={"database": e.__str__()})
                    finally:
                        c.close()
