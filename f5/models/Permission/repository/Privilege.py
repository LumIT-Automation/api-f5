from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Privilege:

    # Table: privilege



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(id: int) -> dict:
        c = connection.cursor()

        try:
            c.execute("SELECT id, privilege, privilege_type, IFNULL(description, '') AS description FROM privilege WHERE id = %s", [id])

            return DBHelper.asDict(c)[0]
        except IndexError:
            raise CustomException(status=404, payload={"database": "non existent privilege"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def list() -> list:
        c = connection.cursor()

        try:
            c.execute("SELECT id, privilege, privilege_type, IFNULL(description, '') AS description FROM privilege")

            return DBHelper.asDict(c)
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
