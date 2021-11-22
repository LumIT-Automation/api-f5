from django.db import connection

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Privilege:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list() -> list:
        c = connection.cursor()
        try:
            c.execute("SELECT * FROM privilege")

            return DBHelper.asDict(c)
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
