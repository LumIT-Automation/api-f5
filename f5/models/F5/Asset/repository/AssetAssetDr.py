from django.utils.html import strip_tags
from django.db import connection
from django.db import transaction

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper
from f5.helpers.Log import Log


class AssetAssetDr:

    # table: asset_assetdr

    #    `pr_asset_id` int(11) NOT NULL,
    #    `dr_asset_id` int(11) NOT NULL,
    #    `enabled` tinyint(1) NOT NULL,



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def delete(primaryAssetId: int, drAssetId: int) -> None:
        c = connection.cursor()

        try:
            c.execute("DELETE FROM asset_assetdr WHERE pr_asset_id = %s AND dr_asset_id = %s", [
                primaryAssetId,
                drAssetId
            ])
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def modify(primaryAssetId: int, drAssetId: int, enabled: bool) -> None:
        c = connection.cursor()

        try:
            c.execute(
                "UPDATE asset_assetdr SET enabled = % "
                "WHERE pr_asset_id = " + primaryAssetId + " AND dr_asset_id = " + drAssetId, [
                    enabled
                ]
            )
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def list(primaryAssetId: int) -> list:
        c = connection.cursor()

        try:
            c.execute(
                "SELECT assetDR.id, assetDR.address, assetDR.fqdn, assetDR.baseurl, assetDR.tlsverify, assetDR.datacenter, assetDR.environment, assetDR.position "
                "FROM asset AS assetPR "
                "INNER JOIN asset_assetdr ON assetPR.id = asset_assetdr.pr_asset_id "
                "INNER JOIN asset AS assetDR ON assetDR.id = asset_assetdr.dr_asset_id "
                "WHERE pr_asset_id = %s AND asset_assetdr.enabled = 1", [
                    primaryAssetId
                ]
            )

            return DBHelper.asDict(c)
        except IndexError:
            raise CustomException(status=404, payload={"database": "non existent asset"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(primaryAssetId: int, drAssetId: int, enabled: bool) -> None:
        c = connection.cursor()

        try:
            c.execute("INSERT INTO asset_assetdr (`pr_asset_id`, `dr_asset_id`, `enabled`) VALUES (%s, %s, %s)",
                [primaryAssetId, drAssetId, int(enabled)]
            )
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError" \
                    and e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "duplicated values"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
