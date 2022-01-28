from f5.models.repository.Configuration import Configuration as Repository


class Configuration:
    def __init__(self, id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = id
        self.config_type = ""
        self.configuration = ""



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def getByType(configType: str) -> dict:
        try:
            return Repository.get(configType)
        except Exception as e:
            raise e



    @staticmethod
    def rewriteByType(configType: str, data: dict) -> None:
        try:
            Repository.modify(configType, data)
        except Exception as e:
            raise e
