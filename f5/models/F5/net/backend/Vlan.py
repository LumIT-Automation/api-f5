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
            vlan = ApiSupplicant(
                endpoint=f5.baseurl + "tm/net/vlan/" + name,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=silent
            ).get()["payload"]

            if vlan:
                interfaces = ApiSupplicant(
                    endpoint=f5.baseurl + "tm/net/vlan/" + name + "/interfaces/",
                    auth = (f5.username, f5.password),
                    tlsVerify = f5.tlsverify,
                    silent = silent
                ).get()["payload"]
                if interfaces:
                    vlan["interfaces"] = interfaces

            return vlan
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
