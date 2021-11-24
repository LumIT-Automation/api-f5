from f5.models.Permission.Role import Role
from f5.models.Permission.Partition import Partition

from f5.repository.Permission import Permission as Repository


class Permission:
    def __init__(self, permissionId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.permissionId = permissionId



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
            # If partition does not exist, create it (on Permissions database, not F5 endpoint).
            p = Partition(assetId=assetId, partitionName=partitionName)
            if p.exists():
                partitionId = p.info()["id"]
            else:
                partitionId = p.add(assetId, partitionName)

            Repository.modify(self.permissionId, identityGroupId, roleId, partitionId)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository.delete(self.permissionId)
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
    def list() -> dict:
        try:
            return {
                "items": Repository.list()
            }
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
            # If partition does not exist, create it (on Permissions database, not F5 endpoint).
            p = Partition(assetId=assetId, partitionName=partitionName)
            if p.exists():
                partitionId = p.info()["id"]
            else:
                partitionId = p.add(assetId, partitionName)

            Repository.add(identityGroupId, roleId, partitionId)
        except Exception as e:
            raise e
