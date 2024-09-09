import json
import re

from f5.models.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class Profile:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def types(assetId: int, partitionName: str) -> list:
        items = list()

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/profile/?$filter=partition+eq+"+partitionName,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            for m in api.get()["payload"]["items"]:
                matches = re.search(r"profile\/(.*)\?", m["reference"]["link"])
                if matches:
                    profileType = str(matches.group(1)).strip()
                    items.append(profileType)

            return items
        except Exception as e:
            raise e



    @staticmethod
    def info(assetId: int, profileType: str, partitionName: str, profileName: str, subPath: str = "", silent: bool = False) -> dict:
        subPath = subPath.replace('/', '~') + '~' if subPath else ''

        try:
            f5 = Asset(assetId)
            return ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/profile/"+profileType+"/~"+partitionName+"~"+subPath+profileName+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=silent
            ).get()["payload"]

        except Exception as e:
            raise e



    @staticmethod
    def modify(assetId: int, profileType: str, partitionName: str, profileName: str, data, subPath: str = ""):
        subPath = subPath.replace('/', '~') + '~' if subPath else ''

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/profile/"+profileType+"/~"+partitionName+"~"+subPath+profileName+"/",
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
    def delete(assetId: int, profileType: str, partitionName: str, profileName: str, subPath: str = ""):
        subPath = subPath.replace('/', '~') + '~' if subPath else ''

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/profile/"+profileType+"/~"+partitionName+"~"+subPath+profileName+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.delete()
        except Exception as e:
            raise e



    @staticmethod
    def list(assetId: int, partitionName: str, profileType: str) -> dict:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/profile/"+profileType+"/?$filter=partition+eq+"+partitionName,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            return api.get()["payload"]["items"]
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, profileType: str, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/ltm/profile/"+profileType+"/",
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
