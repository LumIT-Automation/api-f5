from typing import List, Dict

from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class PermissionWorkflowPrivilege:

    # Tables: group_workflow_partition, identity_group, workflow, partition, privilege



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def workflowAuthorizationsList(groups: list, workflow: str = "") -> dict:
        o = dict()

        if groups:
            workflowWhere = ""
            c = connection.cursor()

            try:
                args = groups.copy()
                groupWhere = ""
                for g in groups:
                    groupWhere += "identity_group.identity_group_identifier = %s || "

                if workflow:
                    workflowWhere = "AND workflow.workflow = %s "
                    args.append(workflow)

                c.execute(
                    "SELECT IFNULL(workflow.workflow, '') AS workflow, "

                    "IFNULL(GROUP_CONCAT( "
                        "DISTINCT CONCAT(`partition`.id_asset,'::',`partition`.`partition`) "
                        "ORDER BY `partition`.id_asset "
                        "SEPARATOR ',' "
                    "), '') AS assetId_partition "

                    "FROM identity_group "
                    "LEFT JOIN group_workflow_partition ON group_workflow_partition.id_group = identity_group.id "
                    "LEFT JOIN workflow ON workflow.id = group_workflow_partition.id_workflow "
                    "LEFT JOIN `partition` ON `partition`.id = group_workflow_partition.id_partition "
                    "WHERE (" + groupWhere[:-4] + ") " +
                    workflowWhere +
                    "GROUP BY workflow.workflow",
                        args
                )

                items: List[Dict] = DBHelper.asDict(c)
                for item in items:
                    flow = item.get("workflow", "")
                    if flow:
                        o[flow] = []
                        el = item.get("assetId_partition", "")
                        assetId_partition = el.split(",")
                        for ap in assetId_partition:
                                [ a, p ] = ap.split("::")
                                o[flow].append({
                                    "asseId": a,
                                    "partition": p
                                })

                return o
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        return {}



    @staticmethod
    def countUserWorkflowPermissions(groups: list, workflow: str, assetId: int = 0, partitionName: str = "") -> int:
        if workflow and groups:
            assetWhere = ""
            partitionWhere = ""

            c = connection.cursor()

            try:
                args = groups.copy()
                groupWhere = ""
                for g in groups:
                    groupWhere += "identity_group.identity_group_identifier = %s || "

                # Put all the args of the query in a list.
                if assetId:
                    args.append(assetId)
                    assetWhere = "AND `partition`.id_asset = %s "

                if partitionName:
                    args.append(partitionName)
                    partitionWhere = "AND (`partition`.`partition` = %s OR `partition`.`partition` = 'any') " # if "any" appears in the query results so far -> pass.

                args.append(workflow)

                c.execute(
                    "SELECT COUNT(*) AS count "
                    "FROM identity_group "
                    "LEFT JOIN group_workflow_partition ON group_workflow_partition.id_group = identity_group.id "
                    "LEFT JOIN workflow ON workflow.id = group_workflow_partition.id_workflow "
                    "LEFT JOIN workflow_privilege ON workflow_privilege.id_workflow = workflow.id "
                    "LEFT JOIN `partition` ON `partition`.id = group_workflow_partition.id_partition "                      
                    "LEFT JOIN privilege ON privilege.id = workflow_privilege.id_privilege "
                    "WHERE (" + groupWhere[:-4] + ") " +
                    assetWhere +
                    partitionWhere +
                    "AND privilege.privilege = %s ",
                        args
                )

                return DBHelper.asDict(c)[0]["count"]
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        return 0
