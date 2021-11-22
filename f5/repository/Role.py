from django.db import connection

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class Role:
    def __init__(self, roleId: int = 0, roleName: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.roleId = roleId
        self.roleName = roleName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        c = connection.cursor()

        try:
            c.execute("SELECT * FROM role WHERE role = %s", [
                self.roleName
            ])

            return DBHelper.asDict(c)[0]
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(showPrivileges: bool = False) -> list:
        c = connection.cursor()

        try:
            if showPrivileges:
                # Grouping roles' and privileges' values into two columns.
                c.execute(
                    "SELECT role.*, IFNULL(group_concat(DISTINCT privilege.privilege), '') AS privileges "
                    "FROM role "
                    "LEFT JOIN role_privilege ON role_privilege.id_role = role.id "
                    "LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege "
                    "GROUP BY role.role"
                )
            else:
                # Grouping roles' values in a single column.
                c.execute("SELECT * FROM role")

            return DBHelper.asDict(c)
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
