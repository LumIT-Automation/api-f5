import json
import time
from typing import List

from f5.models.F5.Asset.Asset import Asset

from f5.models.F5.ASM.backend.PolicyExporter import PolicyExporter
from f5.models.F5.ASM.backend.PolicyImporter import PolicyImporter

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Exception import CustomException
from f5.helpers.Log import Log


class Policy:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(assetId: int, id: str, silent: bool = False) -> dict:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/policies/"+id+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=silent
            )

            return api.get()["payload"]
        except Exception as e:
            raise e



    @staticmethod
    def list(assetId: int) -> List[dict]:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/policies/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            return api.get()["payload"]["items"]
        except Exception as e:
            raise e



    @staticmethod
    def delete(assetId: int, id: str) -> None:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/policies/"+id+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.delete()
        except Exception as e:
            raise e



    @staticmethod
    def downloadPolicyFileFacade(assetId: int, policyId: str, cleanup: bool = False) -> str:
        return PolicyExporter.downloadPolicyFile(
            assetId=assetId,
            localExportFile=PolicyExporter.createExportFile(
                assetId=assetId,
                policyId=policyId
            ),
            cleanup=cleanup
        )



    @staticmethod
    def importPolicyFacade(assetId: int, policyContent: str, newPolicyName: str, cleanup: bool = False) -> dict:
        return PolicyImporter.importFromLocalFile(
            assetId=assetId,
            localImportFile=PolicyImporter.uploadPolicyData(
                assetId=assetId,
                policyContent=policyContent
            ),
            name=newPolicyName,
            cleanup=cleanup
        )



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
