import base64
import json

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException


class Certificate:
    def __init__(self, assetId: int, partitionName: str, resourceName: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = int(assetId)
        self.partitionName = partitionName
        self.resourceName = resourceName



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self, what):
        if any(w in what for w in ("cert", "key")):
            try:
                f5 = Asset(self.assetId)
                asset = f5.info()

                api = ApiSupplicant(
                    endpoint=asset["baseurl"]+"tm/sys/crypto/"+what+"/~"+self.partitionName+"~"+self.resourceName+"/",
                    auth=(asset["username"], asset["password"]),
                    tlsVerify=asset["tlsverify"]
                )

                api.delete(
                    additionalHeaders={
                        "Content-Type": "application/json",
                    }
                )
            except Exception as e:
                raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, what: str) -> dict:
        o = dict()

        if any(w in what for w in ("cert", "key")):
            try:
                f5 = Asset(assetId)
                asset = f5.info()

                api = ApiSupplicant(
                    endpoint=asset["baseurl"]+"tm/sys/crypto/"+what+"/",
                    auth=(asset["username"], asset["password"]),
                    tlsVerify=asset["tlsverify"]
                )

                o["data"] = api.get()
            except Exception as e:
                raise e

        return o



    @staticmethod
    def install(assetId: int, what: str, data: dict) -> object:
        if any(w in what for w in ("cert", "key")):
            try:
                f5 = Asset(assetId)
                asset = f5.info()

                # Decode base 64 data.
                contentBase64 = data["content_base64"] # base 64 UTF-8.

                content = base64.b64decode(contentBase64).decode('utf-8')
                contentLen = len(content.encode('utf-8'))

                # Upload.
                # F5 needs a raw text payload (no JSON or *form data encoding) with the headers specified below.
                Log.log("Uploading "+what+".")

                api = ApiSupplicant(
                    endpoint=asset["baseurl"]+"shared/file-transfer/uploads/"+str(data["name"]),
                    auth=(asset["username"], asset["password"]),
                    tlsVerify=asset["tlsverify"]
                )
                r = api.post(
                    additionalHeaders={
                        "Content-Range": "0-"+str(contentLen - 1)+"/"+str(contentLen),
                        "Content-Length": str(contentLen),
                        "Content-Type": "application/octet-stream; charset=utf-8",
                    },
                    data=content
                )

                # Successfully uploaded.
                if "remainingByteCount" in r and int(r["remainingByteCount"]) == 0 and "localFilePath" in r and r["localFilePath"]:
                    # Install.
                    Log.log("installing "+what+".")

                    partition = ""
                    if "partition" in data:
                        partition = data["partition"]

                    api = ApiSupplicant(
                        endpoint=asset["baseurl"]+"tm/sys/crypto/"+what+"/",
                        auth=(asset["username"], asset["password"]),
                        tlsVerify=asset["tlsverify"]
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
                    )

                    if "from-local-file" not in r or r["from-local-file"] == "":
                        raise CustomException(status=400, payload={"message": "Install failed."})

                else:
                    raise CustomException(status=400, payload={"message": "Upload failed."})

            except Exception as e:
                raise e

        else:
            raise CustomException(status=400, payload={"message": "Action not specified."})

        return r
