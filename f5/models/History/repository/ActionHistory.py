from django.utils.html import strip_tags
from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper
from f5.helpers.Log import Log


class ActionHistory:

    # Table: log_request



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(username: str, allUsersHistory: bool) -> list:
        j = 0
        c = connection.cursor()

        try:
            if allUsersHistory:
                c.execute("SELECT * FROM log_request ORDER BY date DESC")
            else:
                c.execute("SELECT * FROM log_request WHERE username = %s ORDER BY date DESC", [
                    username
                ])

            items = DBHelper.asDict(c)
            for el in items:
                items[j]["date"] = str(el["date"]) # datetime.datetime() to string.
                j += 1

            return items
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
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
            c.execute("INSERT INTO log_request "+keys+" VALUES ("+s[:-1]+")", values) # user data are filtered by the serializer.
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
