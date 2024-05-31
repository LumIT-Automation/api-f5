import json
from typing import List

from f5.models.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class Folder:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(assetId: int, partitionName: str, name: str) -> dict:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl + "tm/ltm/node/~" + partitionName + "~" + name + "/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )
            return api.get()["payload"]
        except Exception as e:
            raise e



    @staticmethod
    def modify(assetId: int, partitionName: str, nodeName: str, data: dict):
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/node/~"+partitionName+"~"+nodeName+"/",
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
    def delete(assetId: int, partitionName: str, folderName: str):

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl + "tm/sys/folder/~"+partitionName+"~"+folderName+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.delete()
        except Exception as e:
            raise e



    @staticmethod
    def list(assetId: int, partitionName: str, silent: bool = False) -> List[dict]:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl + "tm/sys/folder/?$filter=partition+eq+" + partitionName,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=silent
            )
            return api.get()["payload"]["items"]
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/sys/folder/",
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
