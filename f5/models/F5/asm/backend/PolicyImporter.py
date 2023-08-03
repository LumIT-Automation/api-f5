import json
import time
from random import randrange

from f5.models.Asset.Asset import Asset
from f5.models.F5.asm.backend.PolicyBase import PolicyBase

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Exception import CustomException


class PolicyImporter(PolicyBase):

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def uploadPolicyData(assetId: int, policyContent: bytes) -> str:
        filename = "import-policy-" + str(randrange(0, 9999)) + ".xml"

        streamSize = len(policyContent)
        segmentStart = 0
        delta = 1000000
        segmentEnd = delta if streamSize > delta else streamSize - 1

        PolicyImporter._log(
            f"[AssetID: {assetId}] Uploading policy data (sized {streamSize})..."
        )

        try:
            # Upload policy data as file.
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/file-transfer/uploads/" + filename,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=True
            )

            while True:
                response = api.post(
                    additionalHeaders={
                        "Content-Type": "application/octet-stream",
                        "Content-Range": str(segmentStart) + "-" + str(segmentEnd) + "/" + str(streamSize)
                    },
                    data=policyContent[segmentStart:segmentEnd + 1]
                )["payload"]

                segmentStart = segmentEnd + 1
                segmentEnd = min(segmentStart + delta, streamSize - 1)

                if segmentEnd <= segmentStart:
                    break

            if "remainingByteCount" in response \
                    and int(response["remainingByteCount"]) == 0:
                return filename
            else:
                raise CustomException(status=400, payload={"F5": "Upload policy file error: " + str(response)})
        except Exception as e:
            raise e



    @staticmethod
    def importFromLocalFile(assetId: int, localImportFile: str, name: str, cleanup: bool = False) -> dict:
        timeout = 1800 # [second]

        try:
            f5 = Asset(assetId)

            # Create policy from (pre-imported) file.
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/tasks/import-policy/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            PolicyImporter._log(
                f"[AssetID: {assetId}] Importing policy from local import file {localImportFile} as policy name: {name}..."
            )

            taskInformation = api.post(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "filename": localImportFile,
                    "name": name
                })
            )["payload"]

            # Monitor export file creation (async tasks).
            t0 = time.time()

            while True:
                try:
                    api = ApiSupplicant(
                        endpoint=f5.baseurl+"tm/asm/tasks/import-policy/" + taskInformation["id"] + "/",
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    )

                    PolicyImporter._log(
                        f"[AssetID: {assetId}] Waiting for task to complete..."
                    )

                    taskOutput = api.get()["payload"]
                    taskStatus = taskOutput["status"].lower()
                    if taskStatus == "completed":
                        return taskOutput.get("result", {})
                    if taskStatus == "failure":
                        raise CustomException(status=400, payload={"F5": "Import policy failed"})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"F5": "Import policy timed out"})

                    time.sleep(15)
                except KeyError:
                    raise CustomException(status=400, payload={"F5": "Import policy failed"})
        except Exception as e:
            raise e
        finally:
            if cleanup:
                PolicyImporter._cleanupLocalFile(assetId=assetId, task="import", filename=localImportFile)
