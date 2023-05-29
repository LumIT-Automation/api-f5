from __future__ import annotations
from typing import List

from f5.models.Permission.Privilege import Privilege

from f5.models.Permission.repository.Role import Role as Repository
from f5.models.Permission.repository.RolePrivilege import RolePrivilege as RolePrivilegeRepository

from f5.helpers.Misc import Misc


class Role:
    def __init__(self, id: int = 0, role: str = "", loadPrivilege: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.role: str = role
        self.description: str = ""

        self.privileges: List[Privilege] = []

        self.__load(loadPrivilege=loadPrivilege)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        return Misc.deepRepr(self)



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(loadPrivilege: bool = False) -> List[Role]:
        roles = []

        try:
            for role in Repository.list():
                roles.append(
                    Role(id=role["id"], loadPrivilege=loadPrivilege)
                )

            return roles
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self, loadPrivilege: bool = False) -> None:
        try:
            info = Repository.get(id=self.id, role=self.role)

            if loadPrivilege:
                for privilegeId in RolePrivilegeRepository.rolePrivileges(roleId=self.id):
                    self.privileges.append(
                        Privilege(privilegeId)
                    )
            else:
                del self.privileges

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
