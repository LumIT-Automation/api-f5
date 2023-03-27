from f5.models.History.repository.HistoryDr import HistoryDr as Repository

from f5.helpers.Misc import Misc


class HistoryDr:
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id
        self.pr_asset_id: int = 0
        self.dr_asset_id: int = 0
        self.dr_asset_fqdn: str = ""
        self.username: str = ""
        self.action_name: str = ""
        self.request: str = ""
        self.config_object: str = ""
        self.pr_status: str = ""
        self.dr_status: str = ""
        self.pr_response: str = ""
        self.dr_response: str = ""
        self.pr_date: str = ""
        self.dr_date: str = ""



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(username: str, allUsersHistory: bool) -> list:
        try:
            return Repository.list(username, allUsersHistory)
        except Exception as e:
            raise e



    def modify(self, data: dict) -> None:
        try:
            Repository.modify(self.id, data)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> int:
        try:
            return Repository.add(data)
        except Exception as e:
            raise e
