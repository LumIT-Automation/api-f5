from django.db import connection

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper
from f5.helpers.Log import Log


class AssetAssetDr:

    # table: asset_assetdr

    #  `pr_asset_id` int(11) NOT NULL,
    #  `dr_asset_id` int(11) KEY NOT NULL,
    #  `enabled` tinyint(1) NOT NULL,

    #  PRIMARY KEY (`pr_asset_id`,`dr_asset_id`),
    #  CONSTRAINT `k_dr_asset_id` FOREIGN KEY (`dr_asset_id`) REFERENCES `asset` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    #  CONSTRAINT `k_pr_asset_id` FOREIGN KEY (`pr_asset_id`) REFERENCES `asset` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;



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
                "UPDATE asset_assetdr SET enabled = %s "
                "WHERE pr_asset_id = %s AND dr_asset_id = %s", [
                    int(enabled),
                    primaryAssetId,
                    drAssetId
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
                "SELECT assetDR.id, assetDR.address, assetDR.fqdn, assetDR.baseurl, assetDR.tlsverify, assetDR.datacenter, assetDR.environment, assetDR.position, asset_assetdr.enabled "
                "FROM asset AS assetPR "
                "INNER JOIN asset_assetdr ON assetPR.id = asset_assetdr.pr_asset_id "
                "INNER JOIN asset AS assetDR ON assetDR.id = asset_assetdr.dr_asset_id "
                "WHERE pr_asset_id = %s", [
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
            c.execute("SELECT COUNT(*) as c FROM asset_assetdr WHERE `pr_asset_id` = %s AND `dr_asset_id` = %s", [
                drAssetId,
                primaryAssetId
            ])

            if not DBHelper.asDict(c)[0]["c"]:
                c.execute("INSERT INTO asset_assetdr (`pr_asset_id`, `dr_asset_id`, `enabled`) VALUES (%s, %s, %s)", [
                    primaryAssetId,
                    drAssetId,
                    int(enabled)
                ])
            else:
                raise CustomException(status=400, payload={"database": "forbidden values due to circular path"})
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError":
                    if e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "duplicated values"})
                    if e.args and e.args[0] and e.args[0] == 1452:
                        raise CustomException(status=400, payload={"database": "bad data"})
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
