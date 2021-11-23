from f5.repository.Configuration import Configuration as Repository


class Configuration:
    def __init__(self, configType: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configType = configType



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return dict({
                "data": Repository.get(self.configType)
            })
        except Exception as e:
            raise e



    def rewrite(self, data: dict) -> None:
        try:
            Repository.modify(self.configType, data)
        except Exception as e:
            raise e
