from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Permission:
    def __init__(self, permissionId: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(permissionId)
        self.permissionTable = "group_role_partition"
        self.privilegesList = "role"



        # Tables: group_role_partition, identity_group, role, partition



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def get(self) -> dict:
        c = connection.cursor()

        try:
            c.execute(f"SELECT * FROM {self.permissionTable} WHERE id=%s", [self.id])

            return DBHelper.asDict(c)[0]
        except IndexError:
            raise CustomException(status=404, payload={"database": "Non existent permission"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    def modify(self, identityGroupId: int, privilegesListId: int, partitionId: int) -> None:
        c = connection.cursor()

        try:
            c.execute(f"UPDATE {self.permissionTable} SET id_group=%s, id_{self.privilegesList}=%s, id_partition=%s WHERE id=%s", [
                identityGroupId, # AD or RADIUS group.
                privilegesListId,
                partitionId,
                self.id
            ])
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                raise CustomException(status=400, payload={"database": "Duplicated entry"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    def delete(self) -> None:
        c = connection.cursor()

        try:
            c.execute(f"DELETE FROM {self.permissionTable} WHERE id = %s", [
                self.id
            ])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    """
    SELECT group_role_partition.id, 
        identity_group.name AS identity_group_name, 
        identity_group.identity_group_identifier AS identity_group_identifier, 
        role.role AS role, 
        `partition`.id_asset AS partition_asset, 
        `partition`.`partition` AS partition_name 
    FROM identity_group 
    LEFT JOIN group_role_partition ON group_role_partition.id_group = identity_group.id 
    LEFT JOIN role ON role.id = group_role_partition.id_role 
    LEFT JOIN `partition` ON `partition`.id = group_role_partition.id_partition 
    WHERE role.role IS NOT NULL)
    """
    def list(self) -> list:
        c = connection.cursor()

        try:
            c.execute(
                f"SELECT {self.permissionTable}.id, "
                    "identity_group.name AS identity_group_name, "
                    "identity_group.identity_group_identifier AS identity_group_identifier, "
                    f"{self.privilegesList}.{self.privilegesList}, "                              
                    "`partition`.id_asset AS partition_asset, "
                    "`partition`.`partition` AS partition_name "
                "FROM identity_group "
                f"LEFT JOIN {self.permissionTable} ON {self.permissionTable}.id_group = identity_group.id "
                f"LEFT JOIN {self.privilegesList} ON {self.privilegesList}.id = {self.permissionTable}.id_{self.privilegesList} "
                f"LEFT JOIN `partition` ON `partition`.id = {self.permissionTable}.id_partition "
                f"WHERE {self.privilegesList}.{self.privilegesList} IS NOT NULL")
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



    def add(self, identityGroupId: int,  privilegesListId: int, partitionId: int) -> None:
        c = connection.cursor()

        try:
            c.execute(f"INSERT INTO {self.permissionTable} (id_group, id_{self.privilegesList}, id_partition) VALUES (%s, %s, %s)", [
                identityGroupId, # AD or RADIUS group.
                privilegesListId,
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
