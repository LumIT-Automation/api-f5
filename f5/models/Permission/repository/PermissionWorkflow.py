from f5.models.Permission.repository.Permission import Permission



class PermissionWorkflow(Permission):
    def __init__(self, permissionId: int = 0, *args, **kwargs):
        super().__init__(permissionId, *args, **kwargs)

        self.permissionTable = "group_workflow_partition"
        self.privilegesList = "workflow"

        # Tables: group_workflow_partition, identity_group, workflow, partition