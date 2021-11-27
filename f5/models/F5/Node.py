import json

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class Node:
    def __init__(self, assetId: int, partitionName: str, nodeName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.nodeName = nodeName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, data):
        try:
            f5 = Asset(self.assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/node/~"+self.partitionName+"~"+self.nodeName+"/",
                auth=(asset["username"], asset["password"]),
                tlsVerify=asset["tlsverify"]
            )

            api.patch(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps(data)
            )
        except Exception as e:
            raise e



    def delete(self):
        try:
            f5 = Asset(self.assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/node/~"+self.partitionName+"~"+self.nodeName+"/",
                auth=(asset["username"], asset["password"]),
                tlsVerify=asset["tlsverify"]
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
    def list(assetId: int, partitionName: str, silent: bool = False) -> dict:
        o = dict()

        try:
            f5 = Asset(assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/node/?$filter=partition+eq+"+partitionName,
                auth=(asset["username"], asset["password"]),
                tlsVerify=asset["tlsverify"],
                silent=silent
            )

            o["data"] = api.get()
        except Exception as e:
            raise e

        return o



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/node/",
                auth=(asset["username"], asset["password"]),
                tlsVerify=asset["tlsverify"]
            )

            api.post(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps(data)
            )
        except Exception as e:
            raise e



    @staticmethod
    def getNameFromAddress(assetId: int, partitionName: str, address: str, silent: bool = False) -> str:
        name = ""
        try:
            data = Node.list(assetId, partitionName, silent=silent)
            for nel in data["data"]["items"]:
                if nel["address"] == address:
                    name = nel["name"]

            return name
        except Exception as e:
            raise e
