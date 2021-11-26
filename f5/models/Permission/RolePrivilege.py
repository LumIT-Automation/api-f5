class RolePrivilege:
    def __init__(self, roleId: int, privilegeId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.roleId = roleId
        self.privilegeId = privilegeId
