from f5.models.Permission.Workflow import Workflow
from f5.models.Permission.Partition import Partition
from f5.models.Permission.IdentityGroup import IdentityGroup

from f5.models.Permission.repository.PermissionWorkflow import PermissionWorkflow as Repository
from f5.models.Permission.repository.PermissionWorkflowPrivilege import PermissionWorkflowPrivilege as PermissionPrivilegeRepository

from f5.helpers.Exception import CustomException


class PermissionWorkflow:

    # IdentityGroupWorkflowPartition

    def __init__(self, permissionId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(permissionId)
        self.identityGroup: IdentityGroup
        self.workflow: Workflow
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

        try:
            for gr in groups:
                if gr.lower() == "automation.local":
                    return True
            return bool(
                PermissionPrivilegeRepository.countUserWorkflowPermissions(groups, action, assetId, partition)
            )

        except Exception as e:
            raise e



    @staticmethod
    def workflowPermissionsDataList(filters: dict = None) -> list:
        filters = filters or {}

        try:
            return Repository().list(filters = filters)
        except Exception as e:
            raise e



    @staticmethod
    def workflowAuthorizationsList(groups: list, workflow: str = "") -> dict:

        # Superadmin's group.
        for gr in groups:
            if gr.lower() == "automation.local":
                return {
                    "any": [
                        {
                            "assetId": 0,
                            "partition": "any"
                        }
                    ]
                }

        try:
            return PermissionPrivilegeRepository.workflowAuthorizationsList(groups=groups, workflow=workflow)
        except Exception as e:
            raise e



    @staticmethod
    def addFacade(identityGroupId: str, workflow: str, partitionInfo: dict) -> None:
        partitionAssetId = int(partitionInfo.get("assetId", ""))
        partitionName = partitionInfo.get("name", "")

        try:
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

            PermissionWorkflow.__add(
                identityGroup=IdentityGroup(identityGroupIdentifier=identityGroupId),
                workflow=Workflow(workflow=workflow),
                partition=partition
            )
        except Exception as e:
            raise e



    @staticmethod
    def modifyFacade(permissionId: int, identityGroupId: str, workflow: str, partitionInfo: dict) -> None:
        partitionAssetId = int(partitionInfo.get("assetId", ""))
        partitionName = partitionInfo.get("name", "")

        try:
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

            PermissionWorkflow(permissionId).__modify(
                identityGroup=IdentityGroup(identityGroupIdentifier=identityGroupId),
                workflow=Workflow(workflow=workflow),
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
            self.workflow = Workflow(id=info["id_workflow"])
            self.partition = Partition(id=info["id_partition"])
        except Exception as e:
            raise e



    def __modify(self, identityGroup: IdentityGroup, workflow: Workflow, partition: Partition) -> None:
        try:
            Repository(permissionId=self.id).modify(
                identityGroupId=identityGroup.id,
                privilegesListId=workflow.id,
                partitionId=partition.id
            )

            self.__load()
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __add(identityGroup: IdentityGroup, workflow: Workflow, partition: Partition) -> None:
        try:
            Repository().add(
                identityGroupId=identityGroup.id,
                privilegesListId=workflow.id,
                partitionId=partition.id
            )
        except Exception as e:
            raise e