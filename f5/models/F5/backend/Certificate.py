import base64
import json

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException


class Certificate:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def delete(assetId: int, partitionName: str, resourceName: str, what):
        if any(w in what for w in ("cert", "key")):
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
    def list(assetId: int, partitionName: str, what: str) -> dict:
        o = dict()

        if any(w in what for w in ("cert", "key")):
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
        if any(w in what for w in ("cert", "key")):
            try:
                f5 = Asset(assetId)
                # Decode base 64 data.
                contentBase64 = data["content_base64"] # base 64 UTF-8.

                content = base64.b64decode(contentBase64).decode('utf-8')
                contentLen = len(content.encode('utf-8'))

                # Upload.
                # F5 needs a raw text payload (no JSON or *form data encoding) with the headers specified below.
                Log.log("Uploading "+what+".")

                api = ApiSupplicant(
                    endpoint=f5.baseurl+"shared/file-transfer/uploads/"+str(data["name"]),
                    auth=(f5.username, f5.password),
                    tlsVerify=f5.tlsverify
                )
                r = api.post(
                    additionalHeaders={
                        "Content-Range": "0-"+str(contentLen - 1)+"/"+str(contentLen),
                        "Content-Length": str(contentLen),
                        "Content-Type": "application/octet-stream; charset=utf-8",
                    },
                    data=content
                )["payload"]

                # Successfully uploaded.
                if "remainingByteCount" in r and int(r["remainingByteCount"]) == 0 and "localFilePath" in r and r["localFilePath"]:
                    # Install.
                    Log.log("installing "+what+".")

                    api = ApiSupplicant(
                        endpoint=f5.baseurl+"tm/sys/crypto/"+what+"/",
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    )
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
                else:
                    raise CustomException(status=400, payload={"message": "Upload failed."})
            except Exception as e:
                raise e
        else:
            raise CustomException(status=400, payload={"message": "Action not specified."})
