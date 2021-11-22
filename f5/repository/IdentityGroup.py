from django.db import connection
from django.db import transaction
from django.utils.html import strip_tags

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class IdentityGroup:
    def __init__(self, identityGroupIdentifier: str,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.identityGroupIdentifier = identityGroupIdentifier



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        c = connection.cursor()

        try:
            c.execute("SELECT * FROM identity_group WHERE identity_group_identifier = %s", [
                self.identityGroupIdentifier
            ])

            return DBHelper.asDict(c)[0]
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    def modify(self, data: dict) -> None:
        sql = ""
        values = []
        c = connection.cursor()

        if self.__exists():
            for k, v in data.items():
                sql += k + "=%s,"
                values.append(strip_tags(v)) # no HTML allowed.

            values.append(self.identityGroupIdentifier)

            try:
                # Patch identity group.
                c.execute("UPDATE identity_group SET "+sql[:-1]+" WHERE identity_group_identifier = %s",
                    values
                )
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        else:
            raise CustomException(status=404, payload={"database": {"message": "Non existent identity group"}})



    def delete(self) -> None:
        c = connection.cursor()

        if self.__exists():
            try:
                c.execute("DELETE FROM identity_group WHERE identity_group_identifier = %s", [
                    self.identityGroupIdentifier
                ])

                # Foreign keys' on cascade rules will clean the linked items on db.
            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        else:
            raise CustomException(status=404, payload={"database": {"message": "Non existent identity group"}})



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list() -> list:
        # List identity groups with related information regarding the associated roles on partitions
        # and optionally detailed privileges' descriptions.
        c = connection.cursor()

        try:
            c.execute("SELECT "
                "identity_group.*, " 

                "IFNULL(GROUP_CONCAT( "
                    "DISTINCT CONCAT(role.role,'::',CONCAT(partition.id_asset,'::',partition.partition)) " 
                    "ORDER BY role.id "
                    "SEPARATOR ',' "
                "), '') AS roles_partition, "

                "IFNULL(GROUP_CONCAT( "
                    "DISTINCT CONCAT(privilege.privilege,'::',partition.id_asset,'::',partition.partition,'::',privilege.propagate_to_all_asset_partitions,'::',privilege.propagate_to_all_assets) " 
                    "ORDER BY privilege.id "
                    "SEPARATOR ',' "
                "), '') AS privileges_partition "

                "FROM identity_group "
                "LEFT JOIN group_role_partition ON group_role_partition.id_group = identity_group.id "
                "LEFT JOIN role ON role.id = group_role_partition.id_role "
                "LEFT JOIN `partition` ON `partition`.id = group_role_partition.id_partition "
                "LEFT JOIN role_privilege ON role_privilege.id_role = role.id "
                "LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege "
                "GROUP BY identity_group.id"
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

            return DBHelper.asDict(c)
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(data: dict) -> int:
        s = ""
        keys = "("
        values = []

        c = connection.cursor()

        # Build SQL query according to dict fields (only whitelisted fields pass).
        for k, v in data.items():
            s += "%s,"
            keys += k + ","
            values.append(strip_tags(v)) # no HTML allowed.

        keys = keys[:-1]+")"

        try:
            with transaction.atomic():
                # Insert identity group.
                c.execute("INSERT INTO identity_group "+keys+" VALUES ("+s[:-1]+")",
                    values
                )
                return c.lastrowid
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __exists(self) -> int:
        c = connection.cursor()
        try:
            c.execute("SELECT COUNT(*) AS c FROM identity_group WHERE identity_group_identifier = %s", [
                self.identityGroupIdentifier
            ])
            o = DBHelper.asDict(c)

            return int(o[0]['c'])
        except Exception:
            return 0
        finally:
            c.close()
