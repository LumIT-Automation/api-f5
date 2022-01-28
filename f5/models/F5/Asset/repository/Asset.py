from django.utils.html import strip_tags
from django.db import connection
from django.db import transaction
from django.core.cache import cache

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Asset:

    # table: asset

    #   `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #   `address` varchar(64) NOT NULL UNIQUE KEY,
    #   `fqdn` varchar(255) DEFAULT NULL,
    #   `baseurl` varchar(255) NOT NULL,
    #   `tlsverify` tinyint(4) NOT NULL DEFAULT 1,
    #   `datacenter` varchar(255) DEFAULT NULL,
    #   `environment` varchar(255) NOT NULL,
    #   `position` varchar(255) DEFAULT NULL,
    #   `username` varchar(64) NOT NULL DEFAULT '',
    #   `password` varchar(64) NOT NULL DEFAULT ''



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(assetId: int) -> dict:
        if not cache.get("ASSET"+str(assetId)):
            c = connection.cursor()

            try:
                c.execute("SELECT * FROM asset WHERE id = %s", [
                    assetId
                ])

                info = DBHelper.asDict(c)[0]
                cache.set("ASSET"+str(assetId), info, 10)
                return info
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()
        else:
            # Fetching from cache instead of MySQL for when massive threaded calls result in too many sql connections.
            return cache.get("ASSET"+str(assetId))



    @staticmethod
    def modify(assetId: int, data: dict) -> None:
        sql = ""
        values = []

        c = connection.cursor()

        if Asset.__exists(assetId):
            # Build SQL query according to dict fields.
            for k, v in data.items():
                sql += k+"=%s,"
                values.append(strip_tags(v)) # no HTML allowed.

            try:
                c.execute("UPDATE asset SET "+sql[:-1]+" WHERE id = "+str(assetId),
                    values
                )
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        else:
            raise CustomException(status=404, payload={"database": {"message": "Non existent F5 endpoint"}})



    @staticmethod
    def delete(assetId: int) -> None:
        if Asset.__exists(assetId):
            c = connection.cursor()

            try:
                c.execute("DELETE FROM asset WHERE id = %s", [
                    assetId
                ])
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        else:
            raise CustomException(status=404, payload={"database": {"message": "Non existent F5 endpoint"}})



    @staticmethod
    def list() -> list:
        c = connection.cursor()

        try:
            c.execute(
                "SELECT id, address, fqdn, baseurl, tlsverify, datacenter, environment, position "
                "FROM asset"
            )

            return DBHelper.asDict(c)
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(data: dict) -> int:
        s = ""
        keys = "("
        values = []

        c = connection.cursor()

        # Build SQL query according to (validated) input fields.
        for k, v in data.items():
            s += "%s,"
            keys += k+","
            values.append(strip_tags(v)) # no HTML allowed.

        keys = keys[:-1]+")"

        try:
            with transaction.atomic():
                c.execute("INSERT INTO asset "+keys+" VALUES ("+s[:-1]+")",
                    values
                )
                return c.lastrowid
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __exists(assetId: int) -> int:
        c = connection.cursor()

        try:
            c.execute("SELECT COUNT(*) AS c FROM asset WHERE id = %s", [
                assetId
            ])
            o = DBHelper.asDict(c)

            return int(o[0]['c'])
        except Exception:
            return 0
        finally:
            c.close()
