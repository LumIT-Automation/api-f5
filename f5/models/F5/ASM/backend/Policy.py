import json
import time
from datetime import datetime
from typing import List

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Exception import CustomException
from f5.helpers.Log import Log


class Policy:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(assetId: int, id: str) -> dict:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/policies/"+id+"/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
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
    def createExportFile(assetId: int, id: str) -> str:
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
                        "link": "https://localhost/mgmt/tm/asm/policies/" + id
                    }})
            )["payload"]

            # Monitor export file creation (async tasks).
            t0 = time.time()

            while True:
                try:
                    api = ApiSupplicant(
                        endpoint=f5.baseurl+"tm/asm/tasks/export-policy/" + taskInformation["id"] + "/",
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    )

                    taskStatus = api.get()["payload"]["status"].lower()
                    if taskStatus == "completed":
                        break
                    if taskStatus == "failed":
                        raise CustomException(status=400, payload={"F5": f"create export file failed for policy " + id})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"F5": f"create export file timed out for policy " + id})

                    time.sleep(5)
                except KeyError:
                    raise CustomException(status=400, payload={"F5": f"create export file failed for policy " + id})

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
                    "utilCmdArgs": " -c ' for f in $(ls /ts/var/rest/*" + filename + "); do mv -f $f /shared/images/" + filename + "; done'" # internally, <f5user>-filename is given.
                })
            )

            return filename
        except Exception as e:
            raise e



    @staticmethod
    def downloadPolicy(assetId: int, filename: str):
        fullResponse = ""
        fullSize = 0
        segmentStart = 0
        segmentEnd = 0

        try:
            f5 = Asset(assetId)

            while True:
                # Download file (partial content).
                api = ApiSupplicant(
                    endpoint=f5.baseurl+"cm/autodeploy/software-image-downloads/" + filename,
                    auth=(f5.username, f5.password),
                    tlsVerify=f5.tlsverify
                )

                additionalHeaders = {
                    "Content-Type": "application/json",
                }
                if fullSize:
                    additionalHeaders["Content-Range"] = str(segmentStart) + "-" + str(segmentEnd) + "/" + str(fullSize)

                response = api.get(
                    additionalHeaders=additionalHeaders,
                    raw=True
                )

                if response["status"] == 200:
                    fullResponse = response["payload"]
                    break
                if response["status"] == 206:
                    fullResponse += response["payload"]
                    contentRange = response["headers"]["Content-Range"]

                    segment = contentRange.split('/')[0]
                    segmentStart = int(segment.split('-')[0])
                    segmentEnd = int(segment.split('-')[1])
                    if not fullSize:
                        fullSize = int(contentRange.split('/')[1])

                    if segmentEnd == fullSize:
                        break
                    else:
                        segmentStart = segmentEnd + 1
                        segmentEnd = min(segmentStart + 1048575, fullSize - 1)

            return fullResponse
        except Exception as e:
            raise e
