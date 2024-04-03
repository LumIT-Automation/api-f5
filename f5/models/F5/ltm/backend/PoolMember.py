import json
from typing import List

from f5.models.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class PoolMember:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(assetId: int, partition: str, poolName: str, name: str) -> dict:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+partition+"~"+poolName+"/members/~"+partition+"~"+name+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )
            return api.get()["payload"]
        except Exception as e:
            raise e



    @staticmethod
    def stats(assetId: int, partition: str, poolName: str, name: str) -> dict:
        o = dict()

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+partition+"~"+poolName+"/members/~"+partition+"~"+name+"/stats/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )
            r = api.get()["payload"]

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
                            o = v["nestedStats"]["entries"]
                            o["parentState"] = o["status.enabledState"] # rename field as in list.
                            del o["status.enabledState"]

        except Exception as e:
            raise e

        return o



    @staticmethod
    def modify(assetId: int, partition: str, poolName: str, name: str, data: dict) -> None:
        try:
            f5 = Asset(assetId)
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
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+partition+"~"+poolName+"/members/~"+partition+"~"+name+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )
            api.delete()
        except Exception as e:
            raise e



    @staticmethod
    def list(assetId: int, partitionName: str, poolName: str, subPath: str = "") -> dict:
        membersStats: List[dict] = []

        try:
            f5 = Asset(assetId)
            if subPath:
                subPath = subPath + "~"
            apiStats = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+partitionName+"~"+subPath+poolName+"/members/stats/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            o = apiStats.get()["payload"]
            for k, v in o.get("entries", {}).items():
                entries = v["nestedStats"]["entries"]
                membersStats.append({
                    "fullPath": entries["nodeName"]["description"] + ':' + str(entries["port"]["value"]),
                    "enabledState": entries["status.enabledState"]["description"]
                })

            apiList = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+partitionName+"~"+subPath+poolName+"/members/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            o = apiList.get()["payload"]["items"]
            for el in o:
                for m in membersStats:
                    if el["fullPath"] == m["fullPath"]:
                        el["parentState"] = m["enabledState"]

            return o
        except KeyError:
            pass
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, partitionName: str, poolName: str, data: dict) -> None:
        try:
            f5 = Asset(assetId)
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
