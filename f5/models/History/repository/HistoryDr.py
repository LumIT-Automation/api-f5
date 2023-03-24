from django.utils.html import strip_tags
from django.db import connection
from django.db import transaction

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper
from f5.helpers.Log import Log


class HistoryDr:

    # Table: dr_log

    # `id` int(11) NOT NULL AUTO_INCREMENT,
    #  `pr_asset_id` int(11) DEFAULT NULL,
    #  `dr_asset_id` int(11) DEFAULT NULL,
    #  `dr_asset_fqdn` varchar(255) NOT NULL,
    #  `username` varchar(255) NOT NULL,
    #  `action` varchar(255) NOT NULL,
    #  `config_object_type` varchar(255) NOT NULL,
    #  `config_object` varchar(255) NOT NULL,
    #  `pr_status` varchar(32) NOT NULL,
    #  `dr_status` varchar(32) NOT NULL,
    #  `pr_response` varchar(1024) NOT NULL,
    #  `dr_response` varchar(1024) NOT NULL,
    #  `pr_date` datetime NOT NULL DEFAULT current_timestamp(),
    #  `dr_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'




    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(username: str, allUsersHistory: bool) -> list:
        j = 0
        c = connection.cursor()

        try:
            if allUsersHistory:
                c.execute("SELECT id, pr_asset_id, dr_asset_id, dr_asset_fqdn, username, action, "
                          "config_object_type, config_object, pr_status, dr_status, pr_response, dr_response, "
                          "cast(pr_date as char) as pr_date, cast(dr_date as char) as dr_date "
                          "FROM dr_log ORDER BY pr_date DESC")
            else:
                c.execute("SELECT id, pr_asset_id, dr_asset_id, dr_asset_fqdn, username, action, "
                          "config_object_type, config_object, pr_status, dr_status, pr_response, dr_response, "
                          "cast(pr_date as char) as pr_date, cast(dr_date as char) as dr_date "
                          "FROM dr_log WHERE username = %s ORDER BY pr_date DESC", [
                    username
                ])

            items = DBHelper.asDict(c)

            return items
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def modify(historyId: int, data: dict) -> None:
        sql = ""
        values = []

        c = connection.cursor()

        # Build SQL query according to dict fields.
        for k, v in data.items():
            sql += k+"=%s,"
            values.append(strip_tags(v)) # no HTML allowed.

        try:
            c.execute("UPDATE asset SET "+sql[:-1]+" WHERE id = "+str(historyId), values) # user data are filtered by the serializer.
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "duplicated values"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(data: dict) -> int:
        s = ""
        keys = "("
        values = []

        c = connection.cursor()

        # Build SQL query according to input fields.
        for k, v in data.items():
            s += "%s,"
            keys += k+","
            values.append(strip_tags(v)) # no HTML allowed.

        keys = keys[:-1]+")"

        try:
            with transaction.atomic():
                c.execute("INSERT INTO dr_log "+keys+" VALUES ("+s[:-1]+")",
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
