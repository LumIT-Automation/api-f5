from f5.models.Permission.Workflow import Workflow
from f5.models.Permission.Partition import Partition
from f5.models.Permission.IdentityGroup import IdentityGroup

from f5.models.Permission.repository.Permission import Permission as Repository
from f5.models.Permission.repository.Workflow import Workflow as WRepository
from f5.models.Permission.repository.WorkflowPrivilege import WorkflowPrivilege as WorkflowPrivilegeRepository
from f5.models.Permission.Privilege import Privilege

from f5.helpers.Exception import CustomException


class WorkflowPermission:

    # IdentityGroupWorkflowPartition

    def __init__(self, permissionId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(permissionId)
        self.identityGroup: IdentityGroup
        self.workflow: Workflow
        self.partition: Partition

        #self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################
    """
    def delete(self) -> None:
        try:
            Repository.delete(self.id)
            del self
        except Exception as e:
            raise e
    """


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
                    # Check if the given action exists.
                    if action in [ p["privilege"] for p in Privilege.listQuick()]:
                        return True
                    else:
                        return False
            return bool(
                WorkflowPrivilegeRepository.countUserWorkflowPermissions(groups, action, assetId, partition)
            )

        except Exception as e:
            raise e



    @staticmethod
    def workflowPermissionsList(groups: list, workflow: str = "") -> dict:

        # Superadmin's group.
        for gr in groups:
            if gr.lower() == "automation.local":
                return  {
                    "assetId": 0,
                    "partition": "any"
                }

        try:
            return WorkflowPrivilegeRepository.workflowAuthorizationsList(groups=groups, workflow=workflow)
        except Exception as e:
            raise e



    """
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
            info = Repository.get(self.id)

            self.identityGroup = IdentityGroup(id=info["id_group"])
            self.workflow = Workflow(id=info["id_workflow"])
            self.partition = Partition(id=info["id_partition"])
        except Exception as e:
            raise e



    def __modify(self, identityGroup: IdentityGroup, workflow: Workflow, partition: Partition) -> None:
        try:
            Repository.modify(
                self.id,
                identityGroupId=identityGroup.id,
                workflowId=workflow.id,
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
            Repository.add(
                identityGroupId=identityGroup.id,
                workflowId=workflow.id,
                partitionId=partition.id
            )
        except Exception as e:
            raise e
    """