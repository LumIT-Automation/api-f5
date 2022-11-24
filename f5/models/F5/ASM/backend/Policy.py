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
                tlsVerify=f5.tlsverify
            )

            response = api.get(
                raw=True
            )

            if response["status"] == 200:
                fullResponse = response["payload"]

            if response["status"] == 206:
                fileSize = int(response["headers"]["Content-Range"].split('/')[1]) # 1140143.
                fullResponse += response["payload"]

                while segmentEnd < fileSize - 1:
                    segment = response["headers"]["Content-Range"].split('/')[0] # 0-1048575.
                    segmentStart = int(segment.split('-')[1]) + 1
                    segmentEnd = min(segmentStart + delta, fileSize - 1)

                    # Download file (chunk).
                    api = ApiSupplicant(
                        endpoint=f5.baseurl+"cm/autodeploy/software-image-downloads/" + filename,
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    )

                    response = api.get(
                        additionalHeaders={
                            "Content-Range": str(segmentStart) + "-" + str(segmentEnd) + "/" + str(fileSize)
                        },
                        raw=True
                    )

                    fullResponse += response["payload"]

            return fullResponse
        except Exception as e:
            raise e



    @staticmethod
    def uploadPolicy(assetId: int, policyContent: str):
        # policyContent = policyContent.encode("UTF-8")
        fileSize = sys.getsizeof(policyContent)
        segmentStart = 0
        delta = 1000000
        segmentEnd = delta
        fileName = "import-policy-" + str(randrange(0, 9999)) + ".xml"

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"tm/asm/file-transfer/uploads/" + fileName,
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            while segmentEnd < fileSize:
                Log.log(segmentEnd, 'CCCCCCCCCCCCCCCCCCCCCCCCCCCC')
                policyContentChunk = policyContent[segmentStart:segmentEnd + 1]
                # Upload file (chunk).
                response = api.post(
                    additionalHeaders={
                        "Content-Type": "application/xml",
                        "Content-Range": str(segmentStart) + "-" + str(segmentEnd) + "/" + str(fileSize)
                    },
                    data=policyContentChunk
                )["payload"]

                segmentStart = segmentEnd + 1
                segmentEnd = min(segmentStart + delta, fileSize - 1)

                Log.log(response, 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG')
                Log.log(segmentEnd, 'EEEEEEEEEEEEEEEEEEEEEEEEECCCCCC')
        except Exception as e:
            raise e


