from f5.models.Permission.Role import Role
from f5.models.Permission.Partition import Partition
from f5.models.Permission.IdentityGroup import IdentityGroup

from f5.models.Permission.repository.Permission import Permission as Repository
from f5.models.Permission.repository.PermissionPrivilege import PermissionPrivilege as PermissionPrivilegeRepository

from f5.helpers.Exception import CustomException


class Permission:

    # IdentityGroupRolePartition

    def __init__(self, permissionId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(permissionId)
        self.identityGroup: IdentityGroup
        self.role: Role
        self.partition: Partition

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self) -> None:
        try:
            Repository(permissionId=self.id).delete()
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def hasUserPermission(groups: list, action: str, assetId: int = 0, partition: str = "") -> bool:
        # Authorizations' list allowed for any (authenticated) user.
        if action == "authorizations_get":
            return True

        # Superadmin's group.
        for gr in groups:
            if gr.lower() == "automation.local":
                return True

        try:
            return bool(
                PermissionPrivilegeRepository.countUserPermissions(groups, action, assetId, partition)
            )
        except Exception as e:
            raise e



    @staticmethod
    def permissionsDataList() -> list:

        # List of permissions as List[dict].
        # Note. Partition information differ a bit from Partition model (historical reasons).

        #     {
        #         "id": 2,
        #         "identity_group_name": "groupAdmin",
        #         "identity_group_identifier": "cn=groupadmin,cn=users,dc=lab,dc=local",
        #         "role": "admin",
        #         "partition": {
        #             "asset_id": 1,
        #             "name": "any"
        #         }
        #     },

        try:
            return Repository().list()
        except Exception as e:
            raise e



    @staticmethod
    def authorizationsList(groups: list) -> dict:

        # List of authorizations a user has, grouped by authorization type.

        #     "assets_get": [
        #         {
        #             "assetId": "1",
        #             "partition": "any"
        #         }
        #     ],
        #     "partitions_get": [
        #         {
        #             "assetId": "1",
        #             "partition": "any"
        #         }
        #     ],
        #     ...

        superadmin = False
        for gr in groups:
            if gr.lower() == "automation.local":
                superadmin = True
                break

        if superadmin:
            # Superadmin's permissions override.
            authorizations = {
                "any": [
                    {
                        "assetId": 0,
                        "partition": "any"
                    }
                ]
            }
        else:
            try:
                authorizations = PermissionPrivilegeRepository.authorizationsList(groups)
            except Exception as e:
                raise e

        return authorizations



    @staticmethod
    def addFacade(identityGroupId: str, role: str, partitionInfo: dict) -> None:
        partitionAssetId = int(partitionInfo.get("assetId", ""))
        partitionName = partitionInfo.get("name", "")

        try:
            # Get existent or new partition.
            if role == "admin":
                # role admin -> "any" partition, which always exists.
                partition = Partition(assetId=partitionAssetId, name="any")
            else:
                try:
                    # Try retrieving partition.
                    partition = Partition(assetId=partitionAssetId, name=partitionName)
                except CustomException as e:
                    if e.status == 404:
                        try:
                            # If partition does not exist, create it (permissions database).
                            partition = Partition(
                                id=Partition.add(partitionAssetId, partitionName)
                            )
                        except Exception:
                            raise e
                    else:
                        raise e

            Permission.__add(
                identityGroup=IdentityGroup(identityGroupIdentifier=identityGroupId),
                role=Role(role=role),
                partition=partition
            )
        except Exception as e:
            raise e



    @staticmethod
    def modifyFacade(permissionId: int, identityGroupId: str, role: str, partitionInfo: dict) -> None:
        partitionAssetId = int(partitionInfo.get("assetId", ""))
        partitionName = partitionInfo.get("name", "")

        try:
            # Get existent or new partition.
            if role == "admin":
                # role admin -> "any" partition, which always exists.
                partition = Partition(assetId=partitionAssetId, name="any")
            else:
                try:
                    # Try retrieving partition.
                    partition = Partition(assetId=partitionAssetId, name=partitionName)
                except CustomException as e:
                    if e.status == 404:
                        try:
                            # If partition does not exist, create it (permissions database).
                            partition = Partition(
                                id=Partition.add(partitionAssetId, partitionName)
                            )
                        except Exception:
                            raise e
                    else:
                        raise e

            Permission(permissionId).__modify(
                identityGroup=IdentityGroup(identityGroupIdentifier=identityGroupId),
                role=Role(role=role),
                partition=partition
            )
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository(permissionId=self.id).get()

            self.identityGroup = IdentityGroup(id=info["id_group"])
            self.role = Role(id=info["id_role"])
            self.partition = Partition(id=info["id_partition"])
        except Exception as e:
            raise e



    def __modify(self, identityGroup: IdentityGroup, role: Role, partition: Partition) -> None:
        try:
            Repository(permissionId=self.id).modify(
                identityGroupId=identityGroup.id,
                privilegesListId=role.id,
                partitionId=partition.id
            )

            self.__load()
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __add(identityGroup: IdentityGroup, role: Role, partition: Partition) -> None:
        try:
            Repository().add(
                identityGroupId=identityGroup.id,
                privilegesListId=role.id,
                partitionId=partition.id
            )
        except Exception as e:
            raise e
