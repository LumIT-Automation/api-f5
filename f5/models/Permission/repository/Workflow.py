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
    def list(selectWorkflows: list = None) -> List[Dict]:
        selectWorkflows = selectWorkflows or []
        c = connection.cursor()

        sql = "SELECT id, workflow, IFNULL(description, '') AS description FROM workflow"
        try:
            if selectWorkflows:
                sql += " WHERE workflow.workflow = %s"
                for i in range(1,  len(selectWorkflows)):
                    sql += " OR workflow.workflow = %s"

            c.execute(sql, selectWorkflows)

            return DBHelper.asDict(c)
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
