from f5.repository.History import History as Repository


class History:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(username: str, allUsersHistory: bool) -> dict:
        try:
            return dict({
                "data": {
                    "items": Repository.list(username, allUsersHistory)
                }
            })
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> None:
        try:
            Repository.add(data)
        except Exception as e:
            raise e
