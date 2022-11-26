import json

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


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
