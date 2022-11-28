import json
import time
from datetime import datetime

from f5.models.F5.Asset.Asset import Asset

from f5.models.F5.ASM.backend.PolicyBase import PolicyBase

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Exception import CustomException


class PolicyExporter(PolicyBase):

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def createExportFile(assetId: int, policyId: str) -> str:
        timeout = 120 # [second]

        try:
            f5 = Asset(assetId)

            # Create policy export file on assetId for policy id.
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/tasks/export-policy/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            filename = str(datetime.now().strftime("%Y%m%d-%H%M%s")) + "-export.xml"
            taskInformation = api.post(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "filename": filename,
                    "policyReference": {
                        "link": "https://localhost/mgmt/tm/asm/policies/" + policyId
                    }})
            )["payload"]

            PolicyExporter._log(
                f"[AssetID: {assetId}] Creating export file {filename} for policy {policyId}..."
            )

            # Monitor export file creation (async tasks).
            t0 = time.time()

            while True:
                try:
                    api = ApiSupplicant(
                        endpoint=f5.baseurl+"tm/asm/tasks/export-policy/" + taskInformation["id"] + "/",
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    )

                    PolicyExporter._log(
                        f"[AssetID: {assetId}] Waiting for task to complete..."
                    )

                    taskStatus = api.get()["payload"]["status"].lower()
                    if taskStatus == "completed":
                        break
                    if taskStatus == "failed":
                        raise CustomException(status=400, payload={"F5": f"create export file failed for policy " + policyId})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"F5": f"create export file timed out for policy " + policyId})

                    time.sleep(10)
                except KeyError:
                    raise CustomException(status=400, payload={"F5": f"create export file failed for policy " + policyId})

            # Move file internally to be able to download it.
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/util/bash",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            api.post(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "command": "run",
                    "utilCmdArgs": " -c 'for f in $(ls /ts/var/rest/*" + filename + "); do mv -f $f /shared/images/" + filename + "; done'" # internally, <f5user>-filename is given.
                })
            )

            PolicyExporter._log(
                f"[AssetID: {assetId}] Export file for policy {policyId} created: /shared/images/{filename}."
            )

            return filename
        except Exception as e:
            raise e



    @staticmethod
    def downloadPolicyData(assetId: int, localExportFile: str, cleanup: bool = False) -> str:
        fullResponse = ""
        segmentEnd = 0
        delta = 1000000

        PolicyExporter._log(
            f"[AssetID: {assetId}] Downloading data for export file {localExportFile}..."
        )

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"cm/autodeploy/software-image-downloads/" + localExportFile,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=True
            )

            response = api.get(
                raw=True
            )

            if response["status"] == 200:
                fullResponse = response["payload"]

            if response["status"] == 206:
                streamSize = int(response["headers"]["Content-Range"].split('/')[1]) # 1140143.
                fullResponse += response["payload"]

                while segmentEnd < streamSize - 1:
                    segment = response["headers"]["Content-Range"].split('/')[0] # 0-1048575.
                    segmentStart = int(segment.split('-')[1]) + 1
                    segmentEnd = min(segmentStart + delta, streamSize - 1)

                    # Download file (chunks).
                    response = api.get(
                        additionalHeaders={
                            "Content-Range": str(segmentStart) + "-" + str(segmentEnd) + "/" + str(streamSize)
                        },
                        raw=True
                    )

                    fullResponse += response["payload"]

            try:
                PolicyExporter._log("[AssetID: {assetId}] Saving response to file (*nix only)...")
                with open('/tmp/response.xml', 'w') as file:
                    file.write(fullResponse)
            except Exception:
                pass

            return fullResponse
        except Exception as e:
            raise e
        finally:
            if cleanup:
                PolicyExporter._cleanupLocalFile(assetId=assetId, task="export", filename=localExportFile)
