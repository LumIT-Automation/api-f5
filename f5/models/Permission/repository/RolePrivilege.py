from typing import List

from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class RolePrivilege:

    # Tables: role_privilege, role, privilege



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def rolePrivileges(roleId: int) -> List[int]:
        c = connection.cursor()
        privilegesId = []

        try:
            c.execute(
                "SELECT privilege.id FROM role "
                "LEFT JOIN role_privilege ON role_privilege.id_role = role.id "
                "LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege "
                "WHERE role.id = %s", [roleId])

            r = DBHelper.asDict(c)
            for p in r:
                privilegesId.append(p["id"])

            return privilegesId
        except IndexError:
            raise CustomException(status=404, payload={"database": "Non existent role"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
