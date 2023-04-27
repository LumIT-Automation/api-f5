from django.utils.html import strip_tags
from django.db import connection
from django.db import transaction

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper
from f5.helpers.Log import Log


class Asset:

    # Table: asset



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(assetId: int, showPassword: bool) -> dict:
        c = connection.cursor()

        if showPassword:
            select = "*"
        else:
            select = "id, address, fqdn, baseurl, tlsverify, datacenter, environment, position"

        try:
            c.execute("SELECT " + select + " FROM asset WHERE id = %s", [assetId])
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
    def list(showPassword: bool) -> list:
        c = connection.cursor()

        if showPassword:
            select = "*"
        else:
            select = "id, address, fqdn, baseurl, tlsverify, datacenter, environment, position"

        try:
            c.execute("SELECT " + select + " FROM asset")

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
