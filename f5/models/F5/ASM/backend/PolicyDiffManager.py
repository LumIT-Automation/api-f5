import re
import json
import time
import xmltodict

from typing import List, Dict

from f5.models.F5.Asset.Asset import Asset
from f5.models.F5.ASM.backend.PolicyBase import PolicyBase

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Exception import CustomException
from f5.helpers.Log import Log


class PolicyDiffManager(PolicyBase):

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def createDiff(assetId: int, firstPolicy: str, secondPolicy: str) -> dict:
        timeout = 3600 # [second]

        try:
            f5 = Asset(assetId)

            # Create policies' differences.
            api = ApiSupplicant(
                endpoint=f5.baseurl + "tm/asm/tasks/policy-diff/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            taskInformation = api.post(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "firstPolicyReference": {
                        "link": firstPolicy
                    },
                    "secondPolicyReference": {
                        "link": secondPolicy
                    }
                })
            )["payload"]

            PolicyDiffManager._log(
                f"[AssetID: {assetId}] Creating differences between {firstPolicy} and {secondPolicy}..."
            )

            # Monitor export file creation (async tasks).
            t0 = time.time()

            while True:
                try:
                    api = ApiSupplicant(
                        endpoint=f5.baseurl + "tm/asm/tasks/policy-diff/" + taskInformation["id"] + "/",
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    )

                    PolicyDiffManager._log(
                        f"[AssetID: {assetId}] Waiting for task to complete..."
                    )

                    taskOutput = api.get()["payload"]
                    taskStatus = taskOutput["status"].lower()
                    if taskStatus == "completed":
                        out = taskOutput.get("result", {})
                        PolicyDiffManager._log(
                            f"[AssetID: {assetId}] Differences' result: {out}"
                        )

                        return out
                    if taskStatus == "failure":
                        raise CustomException(status=400, payload={"F5": f"policy diff failed"})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"F5": f"policy diff times out"})

                    time.sleep(30)
                except KeyError:
                    raise CustomException(status=400, payload={"F5": f"policy diff failed"})
        except Exception as e:
            raise e



    @staticmethod
    def listDifferences(assetId: int, diffReference: str, firstPolicyXML: str) -> dict:
        page = 0
        items = 100
        differences = []
        completeDifferences = {}

        PolicyDiffManager._log(
            f"[AssetID: {assetId}] Downloading and parsing differences for {diffReference}..."
        )

        try:
            matches = re.search(r"(?<=diffs\/)(.*)(?=\?)", diffReference)
            if matches:
                diffReferenceId = str(matches.group(1)).strip()
                if diffReferenceId:
                    f5 = Asset(assetId)

                    while True:
                        # Collect all differences - request must be paginated.
                        skip = items * page

                        api = ApiSupplicant(
                            endpoint=f5.baseurl + "tm/asm/policy-diffs/" + diffReferenceId + "/differences/?$skip="+str(skip)+"&$top="+str(items),
                            auth=(f5.username, f5.password),
                            tlsVerify=f5.tlsverify,
                            silent=True
                        )

                        response = api.get()["payload"]
                        differences.extend(
                            PolicyDiffManager.__cleanupDifferences(
                                response.get("items", [])
                            )
                        )

                        if int(response.get("pageIndex", 0)) == int(response.get("totalPages", 0)):
                            break
                        else:
                            page += 1

                    completeDifferences = PolicyDiffManager.__differencesAddSourceObjectDate(
                        PolicyDiffManager.__differencesOrderByType(differences),
                        firstPolicyXML
                    )

            return completeDifferences
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __cleanupDifferences(differences: list) -> list:
        diffs = []

        try:
            for el in differences:
                diffs.append({
                    "id": el["id"],
                    "entityType": el["entityKind"].split(":")[3],
                    "diffType": el["diffType"],
                    "firstLastUpdateMicros": el["firstLastUpdateMicros"],
                    "details": el.get("details", []),
                    "entityName": el["entityName"],
                    "canMergeSecondToFirst": el["canMergeSecondToFirst"],
                    "canMergeFirstToSecond": el["canMergeFirstToSecond"],
                })

            return diffs
        except IndexError:
            pass
        except Exception as e:
            raise e



    @staticmethod
    def __differencesOrderByType(differences: list) -> dict:
        diffs: Dict[str, List[dict]] = {}

        try:

            for el in differences:
                entityType = el["entityType"]
                if entityType not in diffs:
                    diffs[entityType] = []

                del(el["entityType"])
                diffs[entityType].append(el)

            return diffs
        except Exception as e:
            raise e



    @staticmethod
    def __differencesAddSourceObjectDate(differences: dict, firstPolicyXML: str) -> dict:
        try:
            xml = xmltodict.parse(firstPolicyXML)

            for k, v in differences.items():
                if k == "filetypes":
                    xmlParameters: List[dict] = xml.get("policy").get("file_types").get("file_type")
                    for el in v:
                        try:
                            el["secondLastUpdateMicros"] = list(filter(lambda i: i["@name"] == el["entityName"], xmlParameters))[0]["last_updated"]
                        except Exception:
                            el["secondLastUpdateMicros"] = 0

                if k == "parameters":
                    xmlParameters: List[dict] = xml.get("policy").get("parameters").get("parameter")
                    for el in v:
                        try:
                            # Read date from xml data, for corresponding object name.
                            el["secondLastUpdateMicros"] = list(filter(lambda i: i["@name"] == el["entityName"], xmlParameters))[0]["last_updated"]
                        except Exception:
                            el["secondLastUpdateMicros"] = 0

                if k == "urls":
                    xmlParameters: List[dict] = xml.get("policy").get("urls").get("url")
                    for el in v:
                        try:
                            el["secondLastUpdateMicros"] = list(filter(lambda i: "[" + i["@protocol"] + "] " + i["@name"] == el["entityName"], xmlParameters))[0]["last_updated"]
                        except Exception:
                            el["secondLastUpdateMicros"] = 0

                if k in ("cookies", "json-profiles", "methods"):
                    for el in v:
                        el["secondLastUpdateMicros"] = 0

            return differences
        except Exception as e:
            raise e
