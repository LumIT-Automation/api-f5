import json
from typing import List

from f5.models.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class Irule:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def modify(assetId: int, partitionName: str, iruleName: str, data):
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/rule/~"+partitionName+"~"+iruleName+"/",
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
    def delete(assetId: int, partitionName: str, iruleName: str):
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/rule/~"+partitionName+"~"+iruleName+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.delete()
        except Exception as e:
            raise e



    @staticmethod
    def list(assetId: int, partitionName: str) -> List[dict]:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/rule/?$filter=partition+eq+"+partitionName,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            return api.get()["payload"]["items"]
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/rule/",
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
