from f5.repository.Privilege import Privilege as Repository


class Privilege:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list() -> dict:
        try:
            return dict({
                "items": Repository.list()
            })
        except Exception as e:
            raise e
