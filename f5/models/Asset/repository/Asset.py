from django.utils.html import strip_tags
from django.db import connection
from django.db import transaction

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Asset:

    # Table: asset



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(assetId: int, showPassword: bool) -> dict:
        c = connection.cursor()

        fields = "id, fqdn, protocol, port, path, tlsverify, baseurl, IFNULL (datacenter, '') AS datacenter, environment, IFNULL (position, '') AS position"
        if showPassword:
            fields += ", IFNULL (username, '') AS username, IFNULL (password, '') AS password"

        try:
            c.execute("SELECT " + fields + " FROM asset WHERE id = %s", [assetId])

            info = DBHelper.asDict(c)[0]
            info["tlsverify"] = bool(info["tlsverify"])

            return info
        except IndexError:
            raise CustomException(status=404, payload={"database": "Non existent asset"})
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

            if k == "tlsverify":
                v = int(v)
            values.append(strip_tags(v)) # no HTML allowed.

        try:
            with transaction.atomic():
                c.execute("UPDATE asset SET " + sql[:-1] + " WHERE id = " + str(assetId), values) # user data are filtered by the serializer.
                c.execute("UPDATE asset SET baseurl=%s WHERE id = " + str(assetId), [
                    Asset.__getBaseurl(assetId)
                ])
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "Duplicated values"})
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

        fields = "id, fqdn, protocol, port, path, tlsverify, baseurl, IFNULL (datacenter, '') AS datacenter, environment, IFNULL (position, '') AS position"
        if showPassword:
            fields += ", IFNULL (username, '') AS username, IFNULL (password, '') AS password"

        try:
            c.execute("SELECT " + fields + " FROM asset")

            l = DBHelper.asDict(c)
            for el in l:
                el["tlsverify"] = bool(el["tlsverify"])

            return l
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

            if k == "tlsverify":
                v = int(v)
            values.append(strip_tags(v)) # no HTML allowed.

        keys = keys[:-1]+")"

        try:
            with transaction.atomic():
                c.execute("INSERT INTO asset " + keys + " VALUES (" + s[:-1] + ")", values) # user data are filtered by the serializer.
                lwId = c.lastrowid

                c.execute("UPDATE asset SET baseurl=%s WHERE id = " + str(lwId), [
                    Asset.__getBaseurl(lwId)
                ])

                return lwId
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "Duplicated values"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __getBaseurl(assetId: int) -> str:
        ai = Asset.get(assetId, showPassword=False)

        return str(ai["protocol"]) + "://" + str(ai["fqdn"]) + ":" + str(ai["port"]) + str(ai["path"])
