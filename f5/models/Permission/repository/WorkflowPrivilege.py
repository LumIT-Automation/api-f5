from typing import List, Dict

from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class WorkflowPrivilege:

    # Tables: workflow_privilege, workflow, privilege



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def workflowPrivileges(workflowId: int) -> List[int]:
        c = connection.cursor()
        workflowsId = []

        try:
            c.execute(
                "SELECT privilege.id FROM workflow "
                "LEFT JOIN workflow_privilege ON workflow_privilege.id_workflow = workflow.id "
                "LEFT JOIN privilege ON privilege.id = workflow_privilege.id_privilege "
                "WHERE workflow.id = %s", [workflowId])

            r = DBHelper.asDict(c)
            for p in r:
                workflowsId.append(p["id"])

            return workflowsId
        except IndexError:
            raise CustomException(status=404, payload={"database": "Non existent workflow"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
