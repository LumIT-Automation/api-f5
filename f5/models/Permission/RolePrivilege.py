class RolePrivilege:
    def __init__(self, id_role: int, id_privilege: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id_role = id_role
        self.id_privilege = id_privilege
