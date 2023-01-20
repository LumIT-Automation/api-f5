from django.db import connection
from django.db import transaction
from django.utils.html import strip_tags

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class IdentityGroup:

    # Table: identity_group

    #   `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    #   `name` varchar(64) NOT NULL KEY,
    #   `identity_group_identifier` varchar(255) DEFAULT NULL UNIQUE KEY



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(id: int, identityGroupIdentifier: str) -> dict:
        c = connection.cursor()

        try:
            if id:
                c.execute("SELECT * FROM identity_group WHERE id = %s", [id])
            if identityGroupIdentifier:
                c.execute("SELECT * FROM identity_group WHERE identity_group_identifier = %s", [
                    identityGroupIdentifier
                ])

            return DBHelper.asDict(c)[0]
        except IndexError:
            raise CustomException(status=404, payload={"database": "non existent identity group"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def modify(id: int, data: dict) -> None:
        sql = ""
        values = []
        c = connection.cursor()

        # %s placeholders and values for SET.
        for k, v in data.items():
            sql += k + "=%s,"
            values.append(strip_tags(v)) # no HTML allowed.

        values.append(id)

        try:
            c.execute("UPDATE identity_group SET " + sql[:-1] + " WHERE id = %s", values) # user data are filtered by the serializer.
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                raise CustomException(status=400, payload={"database": "duplicated identity group"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def delete(id: int) -> None:
        c = connection.cursor()

        try:
            c.execute("DELETE FROM identity_group WHERE id = %s", [id]) # foreign keys' on cascade rules will clean the linked items on db.
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def list() -> list:
        c = connection.cursor()

        try:
            c.execute("SELECT * FROM identity_group")

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

        # Build SQL query according to dict fields (only whitelisted fields pass).
        for k, v in data.items():
            s += "%s,"
            keys += k + ","
            values.append(strip_tags(v)) # no HTML allowed.

        keys = keys[:-1]+")"

        try:
            with transaction.atomic():
                c.execute("INSERT INTO identity_group "+keys+" VALUES ("+s[:-1]+")", values) # user data are filtered by the serializer.

                return c.lastrowid
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "duplicated identity group"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
