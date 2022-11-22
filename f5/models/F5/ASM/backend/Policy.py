import json
from typing import List

from f5.models.F5.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


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
            return api.get()
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

            return api.get()["items"]
        except Exception as e:
            raise e
