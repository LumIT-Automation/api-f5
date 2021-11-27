import json

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class Irule:
    def __init__(self, assetId: int, partitionName: str, iruleName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.iruleName = iruleName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def modify(self, data):
        try:
            f5 = Asset(self.assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/rule/~"+self.partitionName+"~"+self.iruleName+"/",
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
                endpoint=asset["baseurl"]+"tm/ltm/rule/~"+self.partitionName+"~"+self.iruleName+"/",
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
    def list(assetId: int, partitionName: str) -> dict:
        o = dict()

        try:
            f5 = Asset(assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/rule/?$filter=partition+eq+"+partitionName,
                auth=(asset["username"], asset["password"]),
                tlsVerify=asset["tlsverify"]
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
                endpoint=asset["baseurl"]+"tm/ltm/rule/",
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
