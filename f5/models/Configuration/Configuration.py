from typing import List, Dict

from f5.models.Configuration.repository.Configuration import Configuration as Repository


class Configuration:
    def __init__(self, id: int, configType: str = "", value: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id: int = id
        self.config_type: str = configType
        self.value: str = value

        self.__load()



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        return vars(self)



    def delete(self) -> None:
        try:
            Repository.delete(self.id)
            del self
        except Exception as e:
            raise e



    def modify(self, data: dict) -> None:
        try:
            Repository.modify(id=self.id, config_type=data["config_type"], value=data.get("value", ""))
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(configType: list = None) -> List[Dict]:
        configType = configType or []

        try:
            return Repository.list(configType)
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> int:
        try:
            return Repository.add(config_type=data["config_type"], value=data["value"])
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
