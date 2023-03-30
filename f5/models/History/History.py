from f5.models.History.repository.History import History as Repository


class History:
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = int(id)
        self.username: str = ""
        self.action: str = ""
        self.asset_id: int = 0
        self.config_object_type: str = ""
        self.config_object: str = ""
        self.status: str = ""
        self.date: str = ""
        self.dr_replica_flow: str = ""



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def dataList(username: str, allUsersHistory: bool) -> list:
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
