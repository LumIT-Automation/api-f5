from typing import List, Dict

from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Workflow:

    # Table: role



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(id: int, workflow: str) -> dict:
        c = connection.cursor()

        try:
            if id:
                c.execute("SELECT id, workflow, IFNULL(description, '') AS description FROM workflow WHERE id = %s", [id])
            if workflow:
                c.execute("SELECT id, workflow, IFNULL(description, '') AS description FROM workflow WHERE role = %s", [role])

            return DBHelper.asDict(c)[0]
        except IndexError:
            raise CustomException(status=404, payload={"database": "Non existent workflow"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def list() -> List[Dict]:
        c = connection.cursor()

        try:
            c.execute("SELECT id, workflow, IFNULL(description, '') AS description FROM workflow")

            return DBHelper.asDict(c)
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
