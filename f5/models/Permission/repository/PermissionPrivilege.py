from typing import List, Dict

from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class PermissionPrivilege:

    # Tables: group_role_partition, identity_group, role, partition, privilege



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(filterGroups: list = None, showPrivileges: bool = False) -> list:
        # List identity groups with related information regarding the associated roles on partitions,
        # and optionally detailed privileges' descriptions.
        filterGroups = filterGroups or []
        groupWhere = ""
        j = 0

        c = connection.cursor()

        try:
            # Build WHERE clause when filterGroups is specified.
            if filterGroups:
                groupWhere = "WHERE ("
                for _ in filterGroups:
                    groupWhere += "identity_group.identity_group_identifier = %s || "
                groupWhere = groupWhere[:-4] + ") "

            c.execute(
                "SELECT identity_group.*, " 

                "IFNULL(GROUP_CONCAT( "
                    "DISTINCT CONCAT(role.role,'::',CONCAT(partition.id_asset,'::',partition.partition)) " 
                    "ORDER BY role.id "
                    "SEPARATOR ',' "
                "), '') AS roles_partition, "

                "IFNULL(GROUP_CONCAT( "
                    "DISTINCT CONCAT(privilege.privilege,'::',partition.id_asset,'::',partition.partition,'::',privilege.privilege_type) " 
                    "ORDER BY privilege.id "
                    "SEPARATOR ',' "
                "), '') AS privileges_partition "

                "FROM identity_group "
                "LEFT JOIN group_role_partition ON group_role_partition.id_group = identity_group.id "
                "LEFT JOIN role ON role.id = group_role_partition.id_role "
                "LEFT JOIN `partition` ON `partition`.id = group_role_partition.id_partition "
                "LEFT JOIN role_privilege ON role_privilege.id_role = role.id "
                "LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege "
                + groupWhere +
                "GROUP BY identity_group.id",
                      filterGroups
            )

            # Simple start query:
            # SELECT identity_group.*, role.role, privilege.privilege, `partition`.partition
            # FROM identity_group
            # LEFT JOIN group_role_partition ON group_role_partition.id_group = identity_group.id
            # LEFT JOIN role ON role.id = group_role_partition.id_role
            # LEFT JOIN `partition` ON `partition`.id = group_role_partition.id_partition
            # LEFT JOIN role_privilege ON role_privilege.id_role = role.id
            # LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege
            # GROUP BY identity_group.id

            items: List[Dict] = DBHelper.asDict(c)

            # "items": [
            # ...,
            # {
            #    "id": 2,
            #    "name": "groupStaff",
            #    "identity_group_identifier": "cn=groupStaff,cn=users,dc=lab,dc=local",
            #    "roles_partition": "staff::1::Common",
            #    "privileges_partition": "certificates_post::1::Common::1::0,poolMember_get::1::Common::0::0,poolMember_patch::1::Common::0::0,poolMembers_get::1::Common::0::0,poolMemberStats_get::1::Common::0::0,pools_get::1::Common::0::0,partitions_get::1::Common::1::1"
            # },
            # ...
            # ]

            for ln in items:
                if "roles_partition" in items[j]:
                    if "," in ln["roles_partition"]:
                        items[j]["roles_partition"] = ln["roles_partition"].split(",") # "staff::1::partition,...,readonly::2::partition" string to list value: replace into original data structure.
                    else:
                        items[j]["roles_partition"] = [ ln["roles_partition"] ] # simple string to list.

                    # "roles_partition": [
                    #    "admin::1::any",
                    #    "staff::1::PARTITION1",
                    #    "staff::2::PARTITION2"
                    # ]

                    rolesStructure = dict()
                    for rls in items[j]["roles_partition"]:
                        if "::" in rls:
                            rlsList = rls.split("::")
                            if not str(rlsList[0]) in rolesStructure:
                                # Initialize list if not already done.
                                rolesStructure[rlsList[0]] = list()

                            rolesStructure[rlsList[0]].append({
                                "assetId": rlsList[1],
                                "partition": rlsList[2]
                            })

                    items[j]["roles_partition"] = rolesStructure

                    #"roles_partition": {
                    #    "staff": [
                    #        {
                    #            "assetId": 1
                    #            "partition": "PARTITION1"
                    #        },
                    #        {
                    #            "assetId": 2
                    #            "partition": "PARTITION2"
                    #        },
                    #    ],
                    #    "admin": [
                    #        {
                    #            "assetId": 1
                    #            "partition": "any"
                    #        },
                    #    ]
                    #}

                if showPrivileges:
                    # Add detailed privileges' descriptions to the output.
                    if "privileges_partition" in items[j]:
                        if "," in ln["privileges_partition"]:
                            items[j]["privileges_partition"] = ln["privileges_partition"].split(",")
                        else:
                            items[j]["privileges_partition"] = [ ln["privileges_partition"] ]

                        ppStructure = dict()
                        for pls in items[j]["privileges_partition"]:
                            if "::" in pls:
                                pList = pls.split("::")
                                if not str(pList[0]) in ppStructure:
                                    ppStructure[pList[0]] = list()

                                # Differentiate permission type:
                                # global:
                                #     a privilege does not require the asset to be specified <--> it's valid for all assets;
                                #     set "any" for assets value.

                                # asset:
                                #    a privilege does not require the partitions to be specified <--> it's valid for all partitions within the asset;
                                #    set "any" for partitions value.
                                #
                                # object:
                                #     standard.

                                if pList[3]:
                                    if pList[3] == "global":
                                        pList[1] = 0
                                        pList[2] = "any"
                                    if pList[3] == "asset":
                                        pList[2] = "any"

                                if not any(v['assetId'] == 0 for v in ppStructure[pList[0]]): # insert value only if not already present (applied to assetId "0").
                                    ppStructure[pList[0]].append({
                                        "assetId": pList[1],
                                        "partition": pList[2],
                                    })

                        items[j]["privileges_partition"] = ppStructure
                else:
                    del items[j]["privileges_partition"]

                j = j+1

            return items
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def authorizationsList(groups: list) -> dict:
        permissions = list()
        combinedPermissions = dict()

        try:
            o = PermissionPrivilege.list(filterGroups=groups, showPrivileges=True)

            # [
            #   {
            #     "id": 3,
            #     "name": "groupStaff",
            #     "identity_group_identifier": "cn=groupstaff,cn=users,dc=lab,dc=local",
            #     "roles_partition": { ... },
            #     "privileges_partition": { ... }
            #   },
            #   ...
            # ]

            # Collect every permission related to the group in groups.
            for identityGroup in groups:
                for el in o:
                    if "identity_group_identifier" in el:
                        if el["identity_group_identifier"].lower() == identityGroup.lower():
                            permissions.append(el["privileges_partition"])

            # [
            #    {
            #        "assets_get": [
            #            {
            #                "assetId": "1",
            #                "partition": "any"
            #            }
            #        ],
            #        ...
            #    },
            #    {
            #        "assets_get": [
            #            {
            #                "assetId": "1",
            #                "partition": "Common"
            #            }
            #        ],
            #        ...
            #    }
            # ]

            # Clean up structure.
            for el in permissions:
                for k, v in el.items():

                    # Initialize list if not already done.
                    if not str(k) in combinedPermissions:
                        combinedPermissions[k] = list()

                    for innerEl in v:
                        if innerEl not in combinedPermissions[k]:
                            combinedPermissions[k].append(innerEl)

            # {
            #    ...
            #    "assets_get": [
            #        {
            #            "assetId": "1",
            #            "partition": "any"
            #        },
            #        {
            #            "assetId": "1",
            #            "partition": "Common"
            #        },
            #        {
            #            "assetId": "2",
            #            "partition": "Common"
            #        }
            #    ],
            #    ...
            # }

            # Clean up structure.
            for k, v in combinedPermissions.items():
                asset = 0
                for el in v:
                    if el["partition"] == "any":
                        asset = el["assetId"] # assetId for partition "any".

                if asset:
                    for j in range(len(v)):
                        try:
                            if v[j]["assetId"] == asset and v[j]["partition"] != "any":
                                del v[j]
                        except Exception:
                            pass

            # {
            #    ...
            #    "assets_get": [
            #        {
            #            "assetId": "1",
            #            "partition": "any"
            #        },
            #        {
            #            "assetId": "2",
            #            "partition": "Common"
            #        }
            #    ],
            #    ...
            # }
        except Exception as e:
            raise e

        return combinedPermissions



    @staticmethod
    def countUserPermissions(groups: list, action: str, assetId: int = 0, partitionName: str = "") -> int:
        if action and groups:
            assetWhere = ""
            partitionWhere = ""

            c = connection.cursor()

            try:
                # Build the first half of the where condition of the query.
                # Obtain: WHERE (identity_group.identity_group_identifier = %s || identity_group.identity_group_identifier = %s || identity_group.identity_group_identifier = %s || ....)
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

                args.append(action)

                c.execute(
                    "SELECT COUNT(*) AS count "
                    "FROM identity_group "
                    "LEFT JOIN group_role_partition ON group_role_partition.id_group = identity_group.id "
                    "LEFT JOIN role ON role.id = group_role_partition.id_role "
                    "LEFT JOIN role_privilege ON role_privilege.id_role = role.id "
                    "LEFT JOIN `partition` ON `partition`.id = group_role_partition.id_partition "                      
                    "LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege "
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
                    "SELECT workflow.workflow, "

                    "GROUP_CONCAT( "
                        "DISTINCT CONCAT(`partition`.id_asset,'::',`partition`.`partition`) "
                        "ORDER BY `partition`.id_asset "
                        "SEPARATOR ',' "
                    ") AS assetId_partition "

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


