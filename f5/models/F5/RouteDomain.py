from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class RouteDomain:
    def __init__(self, assetId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int) -> dict:
        o = dict()

        try:
            f5 = Asset(assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/net/route-domain",
                auth=(asset["username"], asset["password"]),
                tlsVerify=asset["tlsverify"]
            )

            o["data"] = api.get()
        except Exception as e:
            raise e

        return o
