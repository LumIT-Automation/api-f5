from django.utils.html import strip_tags
from django.db import connection

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Configuration:
    def __init__(self, configType: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configType = configType



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        c = connection.cursor()

        try:
            c.execute("SELECT * FROM configuration WHERE config_type = %s", [
                self.configType
            ])

            return DBHelper.asDict(c)[0]
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    def rewrite(self, data: dict) -> None:
        c = connection.cursor()

        if self.__exists():
            try:
                c.execute("UPDATE configuration SET configuration=%s WHERE config_type=%s", [
                    strip_tags(data["configuration"]),
                    self.configType
                ])
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        else:
            raise CustomException(status=404, payload={"database": {"message": "Non existent configuration"}})



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __exists(self) -> int:
        c = connection.cursor()
        try:
            c.execute("SELECT COUNT(*) AS c FROM configuration WHERE config_type = %s", [
                self.configType
            ])
            o = DBHelper.asDict(c)

            return int(o[0]['c'])
        except Exception:
            return 0
        finally:
            c.close()
