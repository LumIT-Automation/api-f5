from f5.models.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class Vlan:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(assetId: int, name: str, silent: bool = False) -> dict:
        try:
            f5 = Asset(assetId)
            return ApiSupplicant(
                endpoint=f5.baseurl + "tm/net/vlan/" + name,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=silent
            ).get()["payload"]

        except Exception as e:
            raise e



    @staticmethod
    def list(assetId: int) -> list:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/net/vlan",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            return api.get().get("payload", {}).get("items", [])
        except Exception as e:
            raise e
