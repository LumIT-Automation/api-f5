from typing import List

from f5.models.Permission.repository.Role import Role as Repository
from f5.models.Permission.repository.RolePrivilege import RolePrivilege as RolePrivilegeRepository
from f5.models.Permission.repository.Privilege import Privilege


class Role:
    def __init__(self, id: int = 0, role: str = "", loadPrivilege: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.role: str = role
        self.description: str = ""

        self.privileges: List[Privilege] = []

        self.__load(loadPrivilege=loadPrivilege)



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(loadPrivilege: bool = False) -> list:
        try:
            if loadPrivilege:
                return RolePrivilegeRepository.list()
            else:
                return Repository.list()
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self, loadPrivilege: bool = False) -> None:
        try:
            info = Repository.get(id=self.id, role=self.role)

            if loadPrivilege:
                pass #@todo.

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
