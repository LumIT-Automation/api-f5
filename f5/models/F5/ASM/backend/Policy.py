import sys
import json
import time
from random import randrange
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
        segmentEnd = 0
        delta = 1000000

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"cm/autodeploy/software-image-downloads/" + filename,
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

            return fullResponse
        except Exception as e:
            raise e



    @staticmethod
    def uploadPolicy(assetId: int, policyContent: str) -> str:
        streamSize = len(policyContent)
        segmentStart = 0
        delta = 1000000
        segmentEnd = delta

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/file-transfer/uploads/import-policy-" + str(randrange(0, 9999)) + ".xml",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify,
                silent=True
            )

            while True:
                if segmentEnd - segmentStart == delta:
                    r = str(segmentStart) + "-" + str(segmentEnd) + "/" + str(streamSize)
                else:
                    r = str(segmentStart) + "-" + str(segmentEnd - 1) + "/" + str(streamSize)

                response = api.post(
                    additionalHeaders={
                        "Content-Type": "application/xml",
                        "Content-Range": r,
                        "Charset": "utf-8"
                    },
                    data=policyContent[segmentStart:segmentEnd + 1]
                )["payload"]

                segmentStart = segmentEnd + 1
                segmentEnd = min(segmentStart + delta, streamSize)

                if segmentEnd <= segmentStart:
                    break

            return response
        except Exception as e:
            raise e
