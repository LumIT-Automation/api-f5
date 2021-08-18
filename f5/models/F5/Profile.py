import json
import re

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class Profile:
    def __init__(self, assetId: int, partitionName: str, profileType: str, profileName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.profileType = profileType
        self.profileName = profileName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    @staticmethod
    def types(assetId: int, partitionName: str) -> dict:
        items = list()
        o = dict()

        try:
            f5 = Asset(assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/profile/?$filter=partition+eq+"+partitionName,
                auth=asset["auth"],
                tlsVerify=asset["tlsverify"]
            )

            for m in api.get()["items"]:
                matches = re.search(r"profile\/(.*)\?", m["reference"]["link"])
                if matches:
                    profileType = str(matches.group(1)).strip()
                    items.append(profileType)

            o["data"] = {
                "items": items
            }

        except Exception as e:
            raise e

        return o



    def info(self, silent: bool = False):
        o = dict()

        try:
            f5 = Asset(self.assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/profile/"+self.profileType+"/~"+self.partitionName+"~"+self.profileName+"/",
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
                endpoint=asset["baseurl"]+"tm/ltm/profile/"+self.profileType+"/~"+self.partitionName+"~"+self.profileName+"/",
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
                endpoint=asset["baseurl"]+"tm/ltm/profile/"+self.profileType+"/~"+self.partitionName+"~"+self.profileName+"/",
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
    def list(assetId: int, partitionName: str, profileType: str) -> dict:
        o = dict()

        try:
            f5 = Asset(assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/profile/"+profileType+"/?$filter=partition+eq+"+partitionName,
                auth=asset["auth"],
                tlsVerify=asset["tlsverify"]
            )

            o["data"] = api.get()
        except Exception as e:
            raise e

        return o



    @staticmethod
    def add(assetId: int, profileType: str, data: dict) -> None:
        try:
            f5 = Asset(assetId)
            asset = f5.info()

            api = ApiSupplicant(
                endpoint=asset["baseurl"]+"tm/ltm/profile/"+profileType+"/",
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
