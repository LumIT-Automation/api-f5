from typing import List, Dict

from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class RolePrivilege:

    # Table: role_privilege

    #  `id_role` int(11) NOT NULL PRIMARY KEY,
    #  `id_privilege` int(11) NOT NULL KEY

    #   CONSTRAINT `rp_privilege` FOREIGN KEY (`id_privilege`) REFERENCES `privilege` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    #   CONSTRAINT `rp_role` FOREIGN KEY (`id_role`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list() -> List[Dict]:
        j = 0
        c = connection.cursor()

        try:
            # Grouping roles and privileges in two columns.
            c.execute(
                "SELECT role.*, IFNULL(group_concat(DISTINCT privilege.privilege), '') AS privileges "
                "FROM role "
                "LEFT JOIN role_privilege ON role_privilege.id_role = role.id "
                "LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege "
                "GROUP BY role.role"
            )

            items: List[Dict] = DBHelper.asDict(c)
            for el in items:
                if "privileges" in items[j]:
                    if "," in el["privileges"]:
                        items[j]["privileges"] = el["privileges"].split(",")
                    else:
                        items[j]["privileges"] = [ el["privileges"] ]
                j = j+1

            return items
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
