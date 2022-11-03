from typing import List

from f5.models.Permission.repository.Privilege import Privilege as Repository


class Privilege:
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id
        self.privilege = ""
        self.privilege_type = ""
        self.description = ""

        self.__load()



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list() -> list:
        privileges = []

        try:
            for privilege in Repository.list():
                privileges.append(
                    Privilege(privilege["id"])
                )

            return privileges
        except Exception as e:
            raise e



    @staticmethod
    def dataList() -> List[dict]:
        try:
            return Repository.list()
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository.get(self.id)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
