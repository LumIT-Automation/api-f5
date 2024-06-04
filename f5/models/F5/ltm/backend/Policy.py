import json
from typing import List

from f5.models.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class Policy:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(assetId: int, partitionName: str, policyName: str, subPath: str = ""):
        subPath = subPath.replace('/', '~') + '~' if subPath else ''

        try:
            f5 = Asset(assetId)
            endpoint = f5.baseurl+"tm/ltm/policy/~"+partitionName+"~"+subPath+policyName+"/"

            return ApiSupplicant(
                endpoint=endpoint,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            ).get()["payload"]
        except Exception as e:
            raise e



    @staticmethod
    def modify(assetId: int, partitionName: str, policyName: str, data, subPath: str = ""):
        subPath = subPath.replace('/', '~') + '~' if subPath else ''

        try:
            f5 = Asset(assetId)
            endpoint = f5.baseurl+"tm/ltm/policy/~"+partitionName+"~"+subPath+policyName+"/"

            api = ApiSupplicant(
                endpoint=endpoint,
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
    def delete(assetId: int, partitionName: str, policyName: str, subPath: str = ""):
        subPath = subPath.replace('/', '~') + '~' if subPath else ''

        try:
            f5 = Asset(assetId)
            endpoint = f5.baseurl+"tm/ltm/policy/~"+partitionName+"~"+subPath+policyName+"/"

            api = ApiSupplicant(
                endpoint=endpoint,
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
                endpoint=f5.baseurl+"tm/ltm/policy/?$filter=partition+eq+"+partitionName,
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
                endpoint=f5.baseurl+"tm/ltm/policy/",
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



    @staticmethod
    def rules(assetId: int, partitionName: str, policyName: str, subPath: str = ""):
        subPath = subPath.replace('/', '~') + '~' if subPath else ''
        rules: List[dict] = []

        try:
            f5 = Asset(assetId)
            endpoint = f5.baseurl+"tm/ltm/policy/~"+partitionName+"~"+subPath+policyName+"/rules/"

            ruleItems = ApiSupplicant(
                endpoint=endpoint,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            ).get()["payload"]["items"]

            for r in ruleItems:
                actionsEndpoint = f5.baseurl + "tm/ltm/policy/~" + partitionName + "~" + subPath + policyName + "/rules/" + r["name"] + "/actions/"
                conditionsEndpoint = f5.baseurl + "tm/ltm/policy/~" + partitionName + "~" + subPath + policyName + "/rules/" + r["name"] + "/conditions/"

                rules.append({
                    "name": r["name"],
                    "actions": ApiSupplicant(
                        endpoint=actionsEndpoint,
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    ).get()["payload"]["items"],
                    "conditions": ApiSupplicant(
                        endpoint=conditionsEndpoint,
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    ).get()["payload"]["items"]
                })

            return rules
        except Exception as e:
            raise e
