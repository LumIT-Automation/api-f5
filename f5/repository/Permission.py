from django.db import connection

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Permission:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def modify(permissionId: int, identityGroupId: int, roleId: int, partitionId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("UPDATE group_role_partition SET id_group=%s, id_role=%s, id_partition=%s WHERE id=%s", [
                identityGroupId, # AD or RADIUS group.
                roleId,
                partitionId,
                permissionId
            ])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def delete(permissionId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("DELETE FROM group_role_partition WHERE id = %s", [
                permissionId
            ])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def countUserPermissions(groups: list, action: str, assetId: int = 0, partitionName: str = "") -> bool:
        if action and groups:
            args = groups.copy()
            assetWhere = ""
            partitionWhere = ""

            c = connection.cursor()

            try:
                # Build the first half of the where condition of the query.
                # Obtain: WHERE (identity_group.identity_group_identifier = %s || identity_group.identity_group_identifier = %s || identity_group.identity_group_identifier = %s || ....)
                groupWhere = ''
                for g in groups:
                    groupWhere += 'identity_group.identity_group_identifier = %s || '

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
                    "WHERE ("+groupWhere[:-4]+") " +
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

        return False



    @staticmethod
    def list() -> list:
        c = connection.cursor()

        try:
            c.execute(
                "SELECT "
                    "group_role_partition.id, "
                    "identity_group.name AS identity_group_name, "
                    "identity_group.identity_group_identifier AS identity_group_identifier, "
                    "role.role AS role, "
                    "`partition`.id_asset AS partition_asset, "
                    "`partition`.`partition` AS partition_name "
                "FROM identity_group "
                "LEFT JOIN group_role_partition ON group_role_partition.id_group = identity_group.id "
                "LEFT JOIN role ON role.id = group_role_partition.id_role "
                "LEFT JOIN `partition` ON `partition`.id = group_role_partition.id_partition "
                "WHERE role.role IS NOT NULL")
            l = DBHelper.asDict(c)

            for el in l:
                el["partition"] = {
                    "asset_id": el["partition_asset"],
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
    def add(identityGroupId: int, roleId: int, partitionId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("INSERT INTO group_role_partition (id_group, id_role, id_partition) VALUES (%s, %s, %s)", [
                identityGroupId, # AD or RADIUS group.
                roleId,
                partitionId
            ])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def cleanup(identityGroupId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("DELETE FROM group_role_partition WHERE id_group = %s", [
                identityGroupId,
            ])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
