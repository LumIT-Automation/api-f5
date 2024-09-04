from f5.models.Configuration.repository.Configuration import Configuration as Repository

from f5.helpers.Log import Log


class Configuration:
    def __init__(self, configType: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = 0
        self.config_type: str = configType
        self.configuration: dict = {}

        self.__load()



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    def repr(self):
        return vars(self)



    def rewrite(self, data: dict) -> None:
        try:
            Repository.modify(self.id, data.get("configuration", {}))
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self) -> None:
        try:
            info = Repository.get(self.config_type)

            # Set attributes.
            for k, v in info.items():
                setattr(self, k, v)
        except Exception as e:
            raise e
