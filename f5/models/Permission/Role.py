from f5.repository.Role import Role as Repository


class Role:
    def __init__(self, roleId: int = 0, roleName: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.roleId = roleId
        self.roleName = roleName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return Repository.get(roleName=self.roleName)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(showPrivileges: bool = False) -> dict:
        j = 0

        try:
            items = Repository.list(showPrivileges)

            for ln in items:
                if "privileges" in items[j]:
                    if "," in ln["privileges"]:
                        items[j]["privileges"] = ln["privileges"].split(",")
                    else:
                        if ln["privileges"]:
                            items[j]["privileges"] = [ ln["privileges"] ]
                j = j+1

            return dict({
                "items": items
            })
        except Exception as e:
            raise e
