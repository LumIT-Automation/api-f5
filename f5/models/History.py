from django.utils.html import strip_tags
from django.db import connection

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper



class History:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(username: str, allUsersHistory: bool) -> dict:
        c = connection.cursor()
        try:
            if allUsersHistory:
                c.execute("SELECT username, action, asset_id, config_object_type, config_object, status, date FROM log")
            else:
                c.execute("SELECT username, action, asset_id, config_object_type, config_object, status, date FROM log WHERE username = %s", [
                    username
                ])

            return dict({
                "data": {
                    "items": DBHelper.asDict(c)
                }
            })

        except Exception as e:
            raise CustomException(status=400, payload={"database": {"message": e.__str__()}})
        finally:
            c.close()



    @staticmethod
    def add(data: dict) -> None:
        s = ""
        keys = "("
        values = []

        c = connection.cursor()

        # Build SQL query according to dict fields.
        for k, v in data.items():
            s += "%s,"
            keys += k+","
            values.append(strip_tags(v)) # no HTML allowed.

        keys = keys[:-1]+")"

        try:
            c.execute("INSERT INTO log "+keys+" VALUES ("+s[:-1]+")",
                values
            )
        except Exception as e:
            raise CustomException(status=400, payload={"database": {"message": e.__str__()}})
        finally:
            c.close()
