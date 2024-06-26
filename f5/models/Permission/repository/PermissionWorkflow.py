from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class PermissionWorkflow:

    # IdentityGroupWorkflowPartition

    # Tables: group_workflow_partition, identity_group, workflow, partition



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def get(permissionId: int) -> dict:
        c = connection.cursor()

        try:
            c.execute("SELECT * FROM group_workflow_partition WHERE id=%s", [permissionId])

            return DBHelper.asDict(c)[0]
        except IndexError:
            raise CustomException(status=404, payload={"database": "Non existent permission"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def modify(permissionId: int, identityGroupId: int, workflowId: int, partitionId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("UPDATE group_workflow_partition SET id_group=%s, id_workflow=%s, id_partition=%s WHERE id=%s", [
                identityGroupId, # AD or RADIUS group.
                workflowId,
                partitionId,
                permissionId
            ])
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                raise CustomException(status=400, payload={"database": "Duplicated entry"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def delete(permissionId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("DELETE FROM group_workflow_partition WHERE id = %s", [
                permissionId
            ])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def list() -> list:
        c = connection.cursor()

        try:
            c.execute(
                "SELECT "
                    "group_workflow_partition.id, "
                    "identity_group.name AS identity_group_name, "
                    "identity_group.identity_group_identifier AS identity_group_identifier, "
                    "workflow.workflow AS workflow, "
                    "`partition`.id_asset AS partition_asset, "
                    "`partition`.`partition` AS partition_name "
                "FROM identity_group "
                "LEFT JOIN group_workflow_partition ON group_workflow_partition.id_group = identity_group.id "
                "LEFT JOIN workflow ON workflow.id = group_workflow_partition.id_workflow "
                "LEFT JOIN `partition` ON `partition`.id = group_workflow_partition.id_partition "
                "WHERE workflow.workflow IS NOT NULL")
            l = DBHelper.asDict(c)

            for el in l:
                el["partition"] = {
                    "id_asset": el["partition_asset"],
                    "name": el["partition_name"]
                }

                del(el["partition_asset"])
                del(el["partition_name"])

            return l
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(identityGroupId: int, workflowId: int, partitionId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("INSERT INTO group_workflow_partition (id_group, id_workflow, id_partition) VALUES (%s, %s, %s)", [
                identityGroupId, # AD or RADIUS group.
                workflowId,
                partitionId
            ])
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                raise CustomException(status=400, payload={"database": "Duplicated entry"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
