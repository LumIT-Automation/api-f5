from f5.models.F5.repository.RouteDomain import RouteDomain as Repository


class RouteDomain:
    def __init__(self, assetId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int) -> dict:
        try:
            return Repository.list(assetId)
        except Exception as e:
            raise e
