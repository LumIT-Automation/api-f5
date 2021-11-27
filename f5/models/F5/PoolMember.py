import json

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class PoolMember:
    def __init__(self, assetId: int, poolName: str, partition: str, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partition = str(partition)
        self.poolName = str(poolName)
        self.name = str(name)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        o = dict()

        try:
            f5 = Asset(self.assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+self.partition+"~"+self.poolName+"/members/~"+self.partition+"~"+self.name+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )
            o["data"] = api.get()

        except Exception as e:
            raise e

        return o



    def stats(self) -> dict:
        o = dict()

        try:
            f5 = Asset(self.assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+self.partition+"~"+self.poolName+"/members/~"+self.partition+"~"+self.name+"/stats/",
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



    def modify(self, data: dict) -> None:
        try:
            f5 = Asset(self.assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+self.partition+"~"+self.poolName+"/members/~"+self.partition+"~"+self.name+"/",
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



    def delete(self) -> None:
        try:
            f5 = Asset(self.assetId)
            f5.load()

            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/pool/~"+self.partition+"~"+self.poolName+"/members/~"+self.partition+"~"+self.name+"/",
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


    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str, poolName: str) -> dict:
        o = dict()

        if assetId and partitionName and poolName:
            try:
                f5 = Asset(assetId)
                f5.load()

                api = ApiSupplicant(
                    endpoint=f5.baseurl+"tm/ltm/pool/~"+partitionName+"~"+poolName+"/members/",
                    auth=(f5.username, f5.password),
                    tlsVerify=f5.tlsverify
                )
                o["data"] = api.get()
            except Exception as e:
                raise e

        return o



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
