from django.utils.html import strip_tags
from django.db import connection

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Configuration:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(configType: str) -> dict:
        c = connection.cursor()

        try:
            c.execute("SELECT * FROM configuration WHERE config_type = %s", [
                configType
            ])

            return DBHelper.asDict(c)[0]
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def modify(configType: str, data: dict) -> None:
        c = connection.cursor()

        if Configuration.__exists(configType):
            try:
                c.execute("UPDATE configuration SET configuration=%s WHERE config_type=%s", [
                    strip_tags(data["configuration"]),
                    configType
                ])
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        else:
            raise CustomException(status=404, payload={"database": {"message": "Non existent configuration"}})



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __exists(configType: str) -> int:
        c = connection.cursor()
        try:
            c.execute("SELECT COUNT(*) AS c FROM configuration WHERE config_type = %s", [
                configType
            ])
            o = DBHelper.asDict(c)

            return int(o[0]['c'])
        except Exception:
            return 0
        finally:
            c.close()
