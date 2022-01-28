from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class RouteDomain:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int) -> dict:
        try:
            f5 = Asset(assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/net/route-domain",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            return api.get()
        except Exception as e:
            raise e
