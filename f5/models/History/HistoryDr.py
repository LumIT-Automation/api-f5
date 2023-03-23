from f5.models.History.repository.HistoryDr import HistoryDr as Repository


class HistoryDr:
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id
        self.username = ""
        self.action = ""
        self.pr_asset_id = 0
        self.dr_asset_id = 0
        self.dr_asset_fqdn = ""
        self.config_object_type = ""
        self.config_object = ""
        self.pr_status = ""
        self.dr_status = ""
        self.pr_response = ""
        self.dr_response =""
        self.pr_date = ""
        self.dr_date = ""



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
