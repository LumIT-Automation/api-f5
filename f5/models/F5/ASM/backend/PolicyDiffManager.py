import re
import json
import time

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Exception import CustomException
from f5.helpers.Log import Log


class PolicyDiffManager:

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

            # Monitor export file creation (async tasks).
            t0 = time.time()

            while True:
                try:
                    api = ApiSupplicant(
                        endpoint=f5.baseurl + "tm/asm/tasks/policy-diff/" + taskInformation["id"] + "/",
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    )

                    taskOutput = api.get()["payload"]
                    taskStatus = taskOutput["status"].lower()
                    if taskStatus == "completed":
                        return taskOutput.get("result", {})
                    if taskStatus == "failure":
                        raise CustomException(status=400, payload={"F5": f"policy diff failed for {firstPolicy} and {secondPolicy}"})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"F5": f"policy diff times out for {firstPolicy} and {secondPolicy}"})

                    time.sleep(60)
                except KeyError:
                    raise CustomException(status=400, payload={"F5": f"policy diff failed for {firstPolicy} and {secondPolicy}"})
        except Exception as e:
            raise e



    @staticmethod
    def showDifferences(assetId: int, diffReference: str) -> list:
        page = 0
        items = 100
        differences = []

        try:
            matches = re.search(r"(?<=diffs\/)(.*)(?=\?)", diffReference)
            if matches:
                diffReferenceId = str(matches.group(1)).strip()
                if diffReferenceId:
                    f5 = Asset(assetId)

                    while True:
                        skip = items * page

                        api = ApiSupplicant(
                            endpoint=f5.baseurl + "tm/asm/policy-diffs/" + diffReferenceId + "/differences/?$skip="+str(skip)+"&$top="+str(items),
                            auth=(f5.username, f5.password),
                            tlsVerify=f5.tlsverify,
                            silent=True
                        )

                        response = api.get()["payload"]
                        differences.extend(response.get("items", []))

                        if int(response.get("pageIndex", 0)) == int(response.get("totalPages", 0)):
                            break
                        else:
                            page += 1

            return differences
        except Exception as e:
            raise e
