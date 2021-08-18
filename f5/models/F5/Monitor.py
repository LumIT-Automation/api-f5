import json
import re

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class Monitor:
    def __init__(self, assetId: int, partitionName: str, monitorType: str, monitorName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.monitorType = monitorType
        self.monitorName = monitorName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self, silent: bool = False):
        o = dict()

        try:
            f5 = Asset(self.assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/monitor/"+self.monitorType+"/~"+self.partitionName+"~"+self.monitorName+"/",
                auth=asset["auth"],
                tlsVerify=asset["tlsverify"],
                silent=silent
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
                endpoint=asset["baseurl"]+"tm/ltm/monitor/"+self.monitorType+"/~"+self.partitionName+"~"+self.monitorName+"/",
                auth=asset["auth"],
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
                endpoint=asset["baseurl"]+"tm/ltm/monitor/"+self.monitorType+"/~"+self.partitionName+"~"+self.monitorName+"/",
                auth=asset["auth"],
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
    def types(assetId: int, partitionName: str) -> dict:
        items = list()
        o = dict()

        try:
            f5 = Asset(assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/monitor/?$filter=partition+eq+"+partitionName,
                auth=asset["auth"],
                tlsVerify=asset["tlsverify"]
            )

            for m in api.get()["items"]:
                matches = re.search(r"monitor\/(.*)\?", m["reference"]["link"])
                if matches:
                    monitorType = str(matches.group(1)).strip()
                    items.append(monitorType)

            o["data"] = {
                "items": items
            }

        except Exception as e:
            raise e

        return o



    @staticmethod
    def list(assetId: int, partitionName: str, monitorType: str) -> dict:
        o = dict()

        try:
            f5 = Asset(assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/monitor/"+monitorType+"?$filter=partition+eq+"+partitionName,
                auth=asset["auth"],
                tlsVerify=asset["tlsverify"]
            )

            o["data"] = api.get()
        except Exception as e:
            raise e

        return o



    @staticmethod
    def add(assetId: int, monitorType: str, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/monitor/"+monitorType+"/",
                auth=asset["auth"],
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
