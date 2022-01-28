import json

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class PoolMember:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(assetId: int, partition: str, poolName: str, name: str) -> dict:
        try:
            f5 = Asset(assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+partition+"~"+poolName+"/members/~"+partition+"~"+name+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )
            return api.get()
        except Exception as e:
            raise e



    @staticmethod
    def stats(assetId: int, partition: str, poolName: str, name: str) -> dict:
        o = dict()

        try:
            f5 = Asset(assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+partition+"~"+poolName+"/members/~"+partition+"~"+name+"/stats/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )
            r = api.get()

            #{
            #    "kind": "tm:ltm:pool:members:membersstats",
            #    "generation": 1838,
            #    "selfLink": "https://localhost/mgmt/tm/ltm/pool/~Common~phpAuction_pool/members/~Common~192.168.12.33:80/stats?ver=14.1.2.6",
            #    "entries": {
            #        "https://localhost/mgmt/tm/ltm/pool/~Common~phpAuction_pool/members/~Common~192.168.12.33:80/stats": {
            #            "nestedStats": {
            #                "kind": "tm:ltm:pool:members:membersstats",
            #                "selfLink": "https://localhost/mgmt/tm/ltm/pool/~Common~phpAuction_pool/members/~Common~192.168.12.33:80/stats?ver=14.1.2.6",
            #                "entries": {
            #                    "addr": {
            #                        "description": "192.168.12.33"
            #                    },
            #                    ...
            #                }
            #            }
            #        }
            #    }
            #}

            if isinstance(r, dict):
                if "entries" in r:
                    for k, v in r["entries"].items():
                        if "entries" in v["nestedStats"]:
                            o["data"] = v["nestedStats"]["entries"]

        except Exception as e:
            raise e

        return o



    @staticmethod
    def modify(assetId: int, partition: str, poolName: str, name: str, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+partition+"~"+poolName+"/members/~"+partition+"~"+name+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )
            api.put(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps(data)
            )
        except Exception as e:
            raise e



    @staticmethod
    def delete(assetId: int, partition: str, poolName: str, name: str) -> None:
        try:
            f5 = Asset(assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+partition+"~"+poolName+"/members/~"+partition+"~"+name+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )
            api.delete(
                additionalHeaders={
                    "Content-Type": "application/json",
                }
            )
        except Exception as e:
            raise e



    @staticmethod
    def list(assetId: int, partitionName: str, poolName: str) -> dict:
        try:
            f5 = Asset(assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+partitionName+"~"+poolName+"/members/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )
            return api.get()
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, partitionName: str, poolName: str, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+partitionName+"~"+poolName+"/members/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.post(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps(data)
            )
        except Exception as e:
            raise e
