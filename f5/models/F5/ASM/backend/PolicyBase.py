import json

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Log import Log


class PolicyBase:

    ####################################################################################################################
    # protected static methods
    ####################################################################################################################

    @staticmethod
    def _cleanupLocalFile(assetId: int, task: str, filename: str):
        fpath = ""

        if task == "export":
            fpath = "/shared/images/" + filename
        if task == "import":
            fpath = "/ts/var/rest/*" + filename

        if fpath:
            try:
                f5 = Asset(assetId)
                api = ApiSupplicant(
                    endpoint=f5.baseurl + "tm/util/bash",
                    auth=(f5.username, f5.password),
                    tlsVerify=f5.tlsverify
                )

                PolicyBase._log(
                    f"[AssetID: {assetId}] Cleaning up {filename}..."
                )

                api.post(
                    additionalHeaders={
                        "Content-Type": "application/json",
                    },
                    data=json.dumps({
                        "command": "run",
                        "utilCmdArgs": " -c 'rm -f " + fpath + "'"
                    })
                )
            except Exception:
                pass



    @staticmethod
    def _log(message):
        Log.log("[ASM POLICY]" + message, "_")
