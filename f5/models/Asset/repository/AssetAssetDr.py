from django.db import connection

from django.db import transaction

from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper


class AssetAssetDr:

    # Tables: asset_assetdr, asset




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
    def list(primaryAssetId: int, showPassword: bool, showOnlyEnabled: bool = False) -> list:
        condition = ""
        c = connection.cursor()

        if showOnlyEnabled:
            condition = " AND asset_assetdr.enabled = 1"

        if showPassword:
            select = "*"
        else:
            select = "assetDR.id, assetDR.fqdn, assetDR.protocol, assetDR.port, assetDR.path, assetDR.tlsverify, assetDR.baseurl, assetDR.datacenter, assetDR.environment, assetDR.position, asset_assetdr.enabled"

        try:
            c.execute(
                "SELECT " + select + " "
                "FROM asset AS assetPR "
                "INNER JOIN asset_assetdr ON assetPR.id = asset_assetdr.pr_asset_id "
                "INNER JOIN asset AS assetDR ON assetDR.id = asset_assetdr.dr_asset_id "
                "WHERE pr_asset_id = %s" + condition, [
                    primaryAssetId
                ]
            )

            return DBHelper.asDict(c)
        except IndexError:
            raise CustomException(status=404, payload={"database": "Non existent asset"})
        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(primaryAssetId: int, drAssetId: int, enabled: bool) -> None:
        c = connection.cursor()

        try:
            with transaction.atomic():
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
                    raise CustomException(status=400, payload={"database": "Forbidden values due to circular path"})
        except Exception as e:
            if e.__class__.__name__ == "IntegrityError":
                    if e.args and e.args[0] and e.args[0] == 1062:
                        raise CustomException(status=400, payload={"database": "Duplicated values"})
                    if e.args and e.args[0] and e.args[0] == 1452:
                        raise CustomException(status=400, payload={"database": "Bad data"})
            elif e.__class__.__name__ == "CustomException":
                raise e
            else:
                raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()
