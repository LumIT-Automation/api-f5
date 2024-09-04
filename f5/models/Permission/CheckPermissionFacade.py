from f5.models.Permission.Permission import Permission
from f5.models.Permission.PermissionWorkflow import PermissionWorkflow


class CheckPermissionFacade:



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def hasUserPermission(groups: list, action: str, assetId: int = 0, partition: str = "", isWorkflow: bool = False) -> bool:
        try:
            if isWorkflow:
                return bool(
                    PermissionWorkflow.hasUserPermission(groups=groups, action=action, assetId=assetId, partition=partition)
                )
            else:
                return bool(
                    Permission.hasUserPermission(groups=groups, action=action, assetId=assetId, partition=partition)
                )
        except Exception as e:
            raise e
