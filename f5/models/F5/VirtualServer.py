import json

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class VirtualServer:
    def __init__(self, assetId: int, partitionName: str, virtualServerName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.virtualServerName = virtualServerName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self):
        o = dict()

        try:
            f5 = Asset(self.assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/virtual/~"+self.partitionName+"~"+self.virtualServerName+"/",
                auth=(asset["username"], asset["password"]),
                tlsVerify=asset["tlsverify"]
            )

            o["data"] = api.get()
        except Exception as e:
            raise e

        return o



    def policies(self):
        o = dict()

        try:
            f5 = Asset(self.assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/virtual/~"+self.partitionName+"~"+self.virtualServerName+"/policies/",
                auth=(asset["username"], asset["password"]),
                tlsVerify=asset["tlsverify"]
            )

            o["data"] = api.get()
        except Exception as e:
            raise e

        return o



    def profiles(self):
        o = dict()

        try:
            f5 = Asset(self.assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/virtual/~"+self.partitionName+"~"+self.virtualServerName+"/profiles/",
                auth=(asset["username"], asset["password"]),
                tlsVerify=asset["tlsverify"]
            )

            o["data"] = api.get()
        except Exception as e:
            raise e

        return o



    def modify(self, data):
        try:
            f5 = Asset(self.assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/virtual/~"+self.partitionName+"~"+self.virtualServerName+"/",
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
                endpoint=asset["baseurl"]+"tm/ltm/virtual/~"+self.partitionName+"~"+self.virtualServerName+"/",
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
                endpoint=asset["baseurl"]+"tm/ltm/virtual/?$filter=partition+eq+"+partitionName,
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
                endpoint=asset["baseurl"]+"tm/ltm/virtual/",
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
