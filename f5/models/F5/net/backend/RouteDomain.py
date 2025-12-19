from f5.models.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class RouteDomain:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int) -> list:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/net/route-domain",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            return api.get().get("payload", {}).get("items", [])
        except Exception as e:
            raise e
