from f5.models.Permission.Role import Role
from f5.models.Permission.Partition import Partition

from f5.repository.Permission import Permission as Repository


class Permission:

    # IdentityGroupRolePartition

    def __init__(self, id: int, id_group: int = 0, id_role: int = 0, id_partition: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id
        
        self.id_group = id_group
        self.id_role = id_role
        self.id_partition = id_partition



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, identityGroupId: int, role: str, assetId: int, partitionName: str) -> None:
        try:
            if role == "admin":
                # If admin, "any" is the only valid choice for partitionName (on selected assetId).
                partitionName = "any"

            # RoleId.
            r = Role(roleName=role)
            roleId = r.info()["id"]

            # Partition id.
            partitionId = Permission.__getPartition(assetId, partitionName)

            Repository.modify(self.id, identityGroupId, roleId, partitionId)
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
    def hasUserPermission(groups: list, action: str, assetId: int = 0, partitionName: str = "") -> bool:
        # Superadmin's group.
        for gr in groups:
            if gr.lower() == "automation.local":
                return True

        try:
            return bool(
                Repository.countUserPermissions(groups, action, assetId, partitionName)
            )
        except Exception as e:
            raise e



    @staticmethod
    def listIdentityGroupsRolesPartitions() -> list:
        try:
            return Repository.list()
        except Exception as e:
            raise e



    @staticmethod
    def add(identityGroupId: int, role: str, assetId: int, partitionName: str) -> None:
        try:
            if role == "admin":
                # If admin, "any" is the only valid choice for partitionName (on selected assetId).
                partitionName = "any"

            # RoleId.
            r = Role(roleName=role)
            roleId = r.info()["id"]

            # Partition id.
            partitionId = Permission.__getPartition(assetId, partitionName)

            Repository.add(identityGroupId, roleId, partitionId)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    @staticmethod
    def __getPartition(assetId: int, partitionName: str):
        p = Partition(assetId, partitionName)
        if p.exists():
            partitionId = p.info()["id"]
        else:
            # If partition does not exist, create it (on Permissions database, not F5 endpoint).
            partitionId = p.add(assetId, partitionName)

        return partitionId
