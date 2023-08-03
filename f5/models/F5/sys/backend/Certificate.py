import base64
import json

from f5.models.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException


class Certificate:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def delete(assetId: int, partitionName: str, resourceName: str, what: str):
        if what in ("cert", "key"):
            try:
                f5 = Asset(assetId)
                api = ApiSupplicant(
                    endpoint=f5.baseurl+"tm/sys/crypto/"+what+"/~"+partitionName+"~"+resourceName+"/",
                    auth=(f5.username, f5.password),
                    tlsVerify=f5.tlsverify
                )

                api.delete()
            except Exception as e:
                raise e



    @staticmethod
    def list(assetId: int, partitionName: str, what: str) -> list:
        o = dict()

        if what in ("cert", "key"):
            try:
                f5 = Asset(assetId)
                api = ApiSupplicant(
                    endpoint=f5.baseurl+"tm/sys/crypto/"+what+"/?$filter=partition+eq+"+partitionName,
                    auth=(f5.username, f5.password),
                    tlsVerify=f5.tlsverify
                )

                o = api.get()["payload"]["items"]
            except Exception as e:
                raise e

        return o



    @staticmethod
    def install(assetId: int, partition: str, what: str, data: dict) -> None:
        if what in ("cert", "key"):
            try:
                r = Certificate.__uploadResourceFile(assetId=assetId, resourceType=what, resourceName=data["name"], content=base64.b64decode(
                    data["content_base64"]).decode('utf-8')
                )

                f5 = Asset(assetId)
                api = ApiSupplicant(
                    endpoint=f5.baseurl+"tm/sys/crypto/"+what+"/",
                    auth=(f5.username, f5.password),
                    tlsVerify=f5.tlsverify
                )

                Log.log("Installing "+what+"...")
                r = api.post(
                    additionalHeaders={
                        "Content-Type": "application/json" # (F5 dislikes the "charset" specification).
                    },
                    data=json.dumps({
                        "command": "install",
                        "name": str(data["name"]),
                        "from-local-file": str(r["localFilePath"]),
                        "partition": partition
                    })
                )["payload"]

                if "from-local-file" not in r or r["from-local-file"] == "":
                    raise CustomException(status=400, payload={"message": "Install failed."})
            except Exception as e:
                raise e
        else:
            raise NotImplemented



    @staticmethod
    def update(assetId: int, partition: str, resourceName: str, what: str, data: dict) -> None:
        if what in ("cert", "key"):
            try:
                r = Certificate.__uploadResourceFile(assetId=assetId, resourceType=what, resourceName=resourceName, content=base64.b64decode(
                    data["content_base64"]).decode('utf-8')
                )

                f5 = Asset(assetId)
                api = ApiSupplicant(
                    endpoint=f5.baseurl+"tm/sys/file/ssl-"+what+"/~"+partition+"~"+resourceName+"/",
                    auth=(f5.username, f5.password),
                    tlsVerify=f5.tlsverify
                )

                Log.log("Updating "+what+"...")
                api.put(
                    additionalHeaders={
                        "Content-Type": "application/json" # (F5 dislikes the "charset" specification).
                    },
                    data=json.dumps({
                        "source-path": "file:"+str(r["localFilePath"])
                    })
                )

            except Exception as e:
                raise e
        else:
            raise NotImplemented



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __uploadResourceFile(assetId: int, resourceType: str, resourceName: str, content: str) -> dict:
        Log.log("Uploading "+resourceType+"...")

        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl+"shared/file-transfer/uploads/"+str(resourceName),
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            contentLen = len(content.encode('utf-8'))
            r = api.post(
                additionalHeaders={
                    "Content-Range": "0-"+str(contentLen - 1)+"/"+str(contentLen),
                    "Content-Length": str(contentLen),
                    "Content-Type": "application/octet-stream; charset=utf-8",
                },
                data=content # raw text payload.
            )["payload"]
        except Exception as e:
            raise e

        if "remainingByteCount" in r and int(r["remainingByteCount"]) == 0 \
                and "localFilePath" in r and r["localFilePath"]:
            return r
        else:
            raise CustomException(status=400, payload={"message": "Upload failed."})
