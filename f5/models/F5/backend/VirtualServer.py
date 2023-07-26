import json
from typing import List

from f5.models.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class VirtualServer:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(assetId: int, partitionName: str, virtualServerName: str) -> dict:
        try:
            f5 = Asset(assetId)
            items = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/virtual/~"+partitionName+"~"+virtualServerName+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            ).get()["payload"]

            return items
        except Exception as e:
            raise e



    @staticmethod
    def policies(assetId: int, partitionName: str, virtualServerName: str) -> List[dict]:
        try:
            f5 = Asset(assetId)
            items = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/virtual/~"+partitionName+"~"+virtualServerName+"/policies/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            ).get()["payload"]["items"]

            return items
        except Exception as e:
            raise e



    @staticmethod
    def profiles(assetId: int, partitionName: str, virtualServerName: str) -> List[dict]:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/virtual/~"+partitionName+"~"+virtualServerName+"/profiles/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            return api.get()["payload"]["items"]
        except Exception as e:
            raise e



    @staticmethod
    def modify(assetId: int, partitionName: str, virtualServerName: str, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/virtual/~"+partitionName+"~"+virtualServerName+"/",
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
    def delete(assetId: int, partitionName: str, virtualServerName: str) -> None:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/virtual/~"+partitionName+"~"+virtualServerName+"/",
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
            items = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/virtual/?$filter=partition+eq+"+partitionName,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            ).get()["payload"]["items"]

            return items
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/virtual/",
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
