from f5.models.Permission.repository.IdentityGroup import IdentityGroup as Repository
from f5.models.Permission.repository.PermissionPrivilege import PermissionPrivilege as PermissionPrivilegeRepository


class IdentityGroup:
    def __init__(self, id: int = 0, identityGroupIdentifier: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.name: str = ""
        self.identity_group_identifier: str = identityGroupIdentifier

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, data: dict) -> None:
        try:
            Repository.modify(self.id, data)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository.delete(self.id)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def dataList() -> list:
        try:
            return Repository.list()
        except Exception as e:
            raise e



    @staticmethod
    def listWithPermissionsPrivileges(showPrivileges: bool = False) -> list:
        # List identity groups with related information regarding the associated roles on partitions,
        # and optionally detailed privileges' descriptions.
        try:
            return PermissionPrivilegeRepository.list(showPrivileges=showPrivileges)
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> None:
        try:
            Repository.add(data)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository.get(self.id, self.identity_group_identifier)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
