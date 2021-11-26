from f5.repository.Privilege import Privilege as Repository


class Privilege:
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id
        self.privilege = ""
        self.privilege_type = ""
        self.description = ""



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list() -> dict:
        try:
            return dict({
                "items": Repository.list()
            })
        except Exception as e:
            raise e
