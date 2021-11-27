from f5.repository.History import History as Repository


class History:
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id
        self.username = ""
        self.action = ""
        self.asset_id = 0
        self.config_object_type = ""
        self.config_object = ""
        self.status = ""
        self.date = ""



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(username: str, allUsersHistory: bool) -> list:
        try:
            return Repository.list(username, allUsersHistory)
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> None:
        try:
            Repository.add(data)
        except Exception as e:
            raise e
