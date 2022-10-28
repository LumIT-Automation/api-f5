from django.db import connection
from django.db import transaction

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Partition:

    # Table: partition

    #   `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #   `id_asset` int(11) NOT NULL KEY,
    #   `partition` varchar(64) NOT NULL,
    #   `description` varchar(255) DEFAULT NULL
    #
    #   UNIQUE KEY `id_asset` (`id_asset`,`partition`)



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(id: int = 0, assetId: int = 0, partition: str = "") -> dict:
        c = connection.cursor()

        try:
            if id:
                c.execute("SELECT * FROM `partition` WHERE id = %s", [id])
            if assetId and partition:
                c.execute("SELECT * FROM `partition` WHERE `partition` = %s AND id_asset = %s", [partition, assetId])

            return DBHelper.asDict(c)[0]
        except IndexError:
            raise CustomException(status=404, payload={"database": "non existent partition"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def delete(id: int) -> None:
        c = connection.cursor()

        try:
            c.execute("DELETE FROM `partition` WHERE `id` = %s", [id])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(assetId, partition) -> int:
        c = connection.cursor()

        try:
            with transaction.atomic():
                c.execute("INSERT INTO `partition` (id_asset, `partition`) VALUES (%s, %s)", [
                    assetId,
                    partition
                ])

                return c.lastrowid
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
