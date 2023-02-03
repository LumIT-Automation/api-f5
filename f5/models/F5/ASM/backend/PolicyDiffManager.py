import re
import json
import time

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
    def createDiff(assetId: int, destinationPolicyId: str, importedPolicyId: str) -> str:
        diffReference = ""
        timeout = 3600 # [second]

        try:
            f5 = Asset(assetId)

            # Create policies' differences.
            api = ApiSupplicant(
                endpoint=f5.baseurl + "tm/asm/tasks/policy-diff/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            PolicyDiffManager._log(
                f"[AssetID: {assetId}] Creating differences between {destinationPolicyId} and {importedPolicyId}..."
            )

            taskInformation = api.post(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "firstPolicyReference": {
                        "link": "https://localhost/mgmt/tm/asm/policies/" + importedPolicyId
                    },
                    "secondPolicyReference": {
                        "link": "https://localhost/mgmt/tm/asm/policies/" + destinationPolicyId
                    }
                })
            )["payload"]

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
                        result = taskOutput.get("result", {})
                        PolicyDiffManager._log(
                            f"[AssetID: {assetId}] Differences' result: {result}"
                        )

                        matches = re.search(r"(?<=diffs\/)(.*)(?=\?)", result.get("policyDiffReference", {}).get("link", ""))
                        if matches:
                            diffReference = str(matches.group(1)).strip()

                        return diffReference
                    if taskStatus == "failure":
                        raise CustomException(status=400, payload={"F5": "policy diff failed: " + str(taskOutput.get("result", {}).get("message", "--"))})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"F5": "policy diff timed out"})

                    time.sleep(20)
                except KeyError:
                    raise CustomException(status=400, payload={"F5": "policy diff failed"})
        except Exception as e:
            raise e



    @staticmethod
    def listDifferences(sourceAssetId: int, sourcePolicyId: str, destinationAssetId: int, diffReferenceId: str) -> dict:
        page = 0
        items = 100
        differences = []

        PolicyDiffManager._log(
            f"[AssetID: {destinationAssetId}] Downloading and parsing differences for {diffReferenceId}..."
        )

        try:
            f5 = Asset(destinationAssetId)

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

                totalPages = response.get("totalPages", 0)
                if totalPages:
                    if int(response.get("pageIndex", 0)) == int(totalPages):
                        break
                    else:
                        page += 1
                else:
                    break

            completeDifferences = PolicyDiffManager.__differencesAddSourceObjectDate(
                PolicyDiffManager.__differencesOrderByType(differences),
                sourceAssetId,
                sourcePolicyId
            )

            return completeDifferences
        except Exception as e:
            raise e



    @staticmethod
    def mergeDifferences(assetId: int, diffReferenceId: str) -> None:
        timeout = 3600 # [second]

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl + "tm/asm/tasks/policy-merge/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            PolicyDiffManager._log(
                f"[AssetID: {assetId}] Merging differences..."
            )

            taskInformation = api.post(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "policyDiffReference": {
                        "link": "/mgmt/tm/asm/policy-diffs/" + diffReferenceId,
                    },
                    "addMissingEntitiesToFirst": False,
                    "addMissingEntitiesToSecond": True, # destination.
                    "handleCommonEntities": "accept-from-first",
                    "handleMissingEntities": "accept-from-first"
                })
            )["payload"]

            # Monitor export file creation (async tasks).
            t0 = time.time()

            while True:
                try:
                    api = ApiSupplicant(
                        endpoint=f5.baseurl + "tm/asm/tasks/policy-merge/" + taskInformation["id"] + "/",
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    )

                    PolicyDiffManager._log(
                        f"[AssetID: {assetId}] Waiting for task to complete..."
                    )

                    taskOutput = api.get()["payload"]
                    taskStatus = taskOutput["status"].lower()
                    if taskStatus == "completed":
                        break
                    if taskStatus == "failure":
                        raise CustomException(status=400, payload={"F5": "policy merge failed"})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"F5": "policy merge timed out"})

                    time.sleep(5)
                except KeyError:
                    raise CustomException(status=400, payload={"F5": "policy merge failed"})
        except Exception as e:
            raise e



    @staticmethod
    def getObjectsIdsFromDiffIds(assetId: int, policyId: str, differences: dict) -> dict:
        elements = dict()

        try:
            # @todo: create and use models.
            try:
                f5 = Asset(assetId)

                PolicyDiffManager._log(
                    f"[AssetID: {assetId}] Getting policy's object ids for diffs..."
                )

                for k, v in differences.items():
                    if v:
                        api = ApiSupplicant(
                            endpoint=f5.baseurl + "tm/asm/policies/" + policyId + "/" + k + "/", # no pagination needed.
                            auth=(f5.username, f5.password),
                            tlsVerify=f5.tlsverify,
                            silent=True
                        )

                        try:
                            o = api.get()["payload"]["items"]

                            for el in v:
                                for elm in o:
                                    valid = False

                                    if k == "signatures":
                                        if elm["signatureReference"]["name"] == el["entityName"]:
                                            valid = True

                                    elif k == "signature-sets":
                                        if elm["signatureSetReference"]["name"] == el["entityName"]:
                                            valid = True

                                    elif k == "server-technologies":
                                        if elm["serverTechnologyReference"]["serverTechnologyName"] == el["entityName"]:
                                            valid = True

                                    elif k == "whitelist-ips":
                                        if elm["ipAddress"]+"/"+elm["ipMask"] == el["entityName"]:
                                            valid = True

                                    elif k == "urls":
                                        if elm["name"] == el["entityName"] \
                                                or "["+elm["protocol"].upper()+"] "+elm["name"] == el["entityName"]:
                                            valid = True

                                    elif "blocking-settings" in k:
                                        if elm["description"] == el["entityName"]:
                                            valid = True

                                    else:
                                        if elm["name"] == el["entityName"]:
                                            valid = True

                                    if valid:
                                        if k not in elements:
                                            elements[k] = list()

                                        elements[k].append(elm["id"])
                        except KeyError:
                            pass
            except Exception as e:
                raise e

            PolicyDiffManager._log(
                f"[AssetID: {assetId}] Objects IDS: {elements}"
            )

            return elements
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __epochS(epoch: str) -> int:
        epoch = int(epoch)

        try:
            if epoch:
                if epoch > 10000000000:
                    epoch = int(epoch / 1000000)
        except Exception:
            pass

        return epoch



    @staticmethod
    def __cleanupDifferences(differences: list) -> list:
        diffs = []

        def cleanDiffType(t):
            if t == "only-in-first":
                return "only-in-source"
            elif t == "only-in-second":
                return "only-in-destination"
            else:
                return t

        def cleanDetails(details):
            clean = list()

            for j in details:
                clean.append({
                    "sourceValue": j.get("firstValue", None),
                    "sourceElement": j.get("firstElement", None),
                    "destinationValue": j.get("secondValue", None),
                    "destinationElement": j.get("secondElement", None),
                    "field": j.get("firstElement", None)
                })
            return clean

        try:
            for el in differences:
                entityType = el["entityKind"].split(":")[3]
                if "blocking-settings" in el["entityKind"]:
                    entityType += "/" + el["entityKind"].split(":")[4]

                o = {
                    "id": el["id"],
                    "entityType": entityType,
                    "entityKind": el["entityKind"],
                    "diffType": cleanDiffType(el["diffType"]),
                    "details": cleanDetails(el.get("details", [])),
                    "entityName": el["entityName"],
                    "canMerge": {
                        "destinationToSource": el["canMergeSecondToFirst"],
                        "sourceToDestination": el["canMergeFirstToSecond"]
                    }
                }

                lastUpdate = PolicyDiffManager.__epochS(el["secondLastUpdateMicros"])
                if lastUpdate:
                    o["destinationLastUpdate"] = lastUpdate

                diffs.append(o)
            return diffs
        except KeyError:
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
    def __differencesAddSourceObjectDate(differences: dict, sourceAssetId: int, sourcePolicyId: str) -> dict:
        try:
            # @todo: create and use models.
            try:
                f5 = Asset(sourceAssetId)
                for k, v in differences.items():
                    if v:
                        api = ApiSupplicant(
                            endpoint=f5.baseurl + "tm/asm/policies/" + sourcePolicyId + "/" + k + "/", # no pagination needed.
                            auth=(f5.username, f5.password),
                            tlsVerify=f5.tlsverify,
                            silent=True
                        )

                        try:
                            o = api.get()["payload"]["items"]

                            for el in v:
                                for elm in o:
                                    valid = False

                                    if k == "signatures":
                                        if elm["signatureReference"]["name"] == el["entityName"]:
                                            valid = True

                                    elif k == "signature-sets":
                                        if elm["signatureSetReference"]["name"] == el["entityName"]:
                                            valid = True

                                    elif k == "server-technologies":
                                        if elm["serverTechnologyReference"]["serverTechnologyName"] == el["entityName"]:
                                            valid = True

                                    elif k == "whitelist-ips":
                                        if elm["ipAddress"]+"/"+elm["ipMask"] == el["entityName"]:
                                            valid = True

                                    elif k == "urls":
                                        if elm["name"] == el["entityName"] \
                                                or "["+elm["protocol"].upper()+"] "+elm["name"] == el["entityName"]:
                                            valid = True

                                    elif "blocking-settings" in k:
                                        if elm["description"] == el["entityName"]:
                                            valid = True

                                    else:
                                        if elm["name"] == el["entityName"]:
                                            valid = True

                                    if valid:
                                        el["sourceLastUpdate"] = PolicyDiffManager.__epochS(elm["lastUpdateMicros"])
                        except KeyError:
                            pass
            except Exception as e:
                raise e

            return differences
        except Exception as e:
            raise e
