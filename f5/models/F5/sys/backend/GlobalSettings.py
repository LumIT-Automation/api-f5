import json
from typing import List

from f5.models.Asset.Asset import Asset

from f5.helpers.ApiSupplicant import ApiSupplicant


class GlobalSettings:

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def info(assetId: int) -> dict:
        try:
            f5 = Asset(assetId)
            api = ApiSupplicant(
                endpoint=f5.baseurl + "tm/sys/global-settings",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )
            return api.get()["payload"]
        except Exception as e:
            raise e




