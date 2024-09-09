import json
import re

from f5.models.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class Monitor:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(assetId, partitionName: str, monitorType: str, monitorName: str, subPath: str = "", silent: bool = False) -> dict:
        subPath = subPath.replace('/', '~') + '~' if subPath else ''

        try:
            f5 = Asset(assetId)
            return ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/monitor/"+monitorType+"/~"+partitionName+"~"+subPath+monitorName+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=silent
            ).get()["payload"]

        except Exception as e:
            raise e



    @staticmethod
    def modify(assetId, partitionName: str, monitorType: str, monitorName: str, data: dict, subPath: str = ""):
        subPath = subPath.replace('/', '~') + '~' if subPath else ''

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/monitor/"+monitorType+"/~"+partitionName+"~"+subPath+monitorName+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.patch(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps(data)
            )
        except Exception as e:
            raise e



    @staticmethod
    def delete(assetId, partitionName: str, monitorType: str, monitorName: str, subPath: str = ""):
        subPath = subPath.replace('/', '~') + '~' if subPath else ''

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/monitor/"+monitorType+"/~"+partitionName+"~"+subPath+monitorName+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.delete()
        except Exception as e:
            raise e



    @staticmethod
    def types(assetId: int, partitionName: str) -> list:
        items = list()

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/monitor/?$filter=partition+eq+"+partitionName,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            for m in api.get()["payload"]["items"]:
                matches = re.search(r"monitor\/(.*)\?", m["reference"]["link"])
                if matches:
                    monitorType = str(matches.group(1)).strip()
                    items.append(monitorType)

            return items
        except Exception as e:
            raise e



    @staticmethod
    def list(assetId: int, partitionName: str, monitorType: str) -> dict:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/monitor/"+monitorType+"?$filter=partition+eq+"+partitionName,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            return api.get()["payload"]["items"]
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, monitorType: str, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/monitor/"+monitorType+"/",
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
