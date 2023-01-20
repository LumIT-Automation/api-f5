from django.utils.html import strip_tags
from django.db import connection
from django.db import transaction

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper
from f5.helpers.Log import Log


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
        c = connection.cursor()

        try:
            c.execute("SELECT * FROM asset WHERE id = %s", [assetId])
            info = DBHelper.asDict(c)[0]

            return info
        except IndexError:
            raise CustomException(status=404, payload={"database": "non existent asset"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def modify(assetId: int, data: dict) -> None:
        assetId = int(assetId)
        sql = ""
        values = []

        c = connection.cursor()

        # Build SQL query according to dict fields.
        for k, v in data.items():
            sql += k+"=%s,"
            values.append(strip_tags(v)) # no HTML allowed.

        try:
            c.execute("UPDATE asset SET "+sql[:-1]+" WHERE id = "+str(assetId), values) # user data are filtered by the serializer.
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "duplicated values"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def delete(assetId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("DELETE FROM asset WHERE id = %s", [assetId])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def purgeAll() -> None:
        from django.conf import settings
        c = connection.cursor()

        try:
            if "sqlite3" in settings.DATABASES["default"]["ENGINE"]:
                c.execute("DELETE FROM asset")
                connection.commit()
                c.execute("UPDATE sqlite_sequence SET seq=0 WHERE name='asset'")
            else:
                c.execute("SET FOREIGN_KEY_CHECKS = 0; TRUNCATE `asset`; SET FOREIGN_KEY_CHECKS = 1")
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



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
                c.execute("INSERT INTO asset "+keys+" VALUES ("+s[:-1]+")", # user data are filtered by the serializer.
                    values
                )
                return c.lastrowid
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "duplicated values"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
