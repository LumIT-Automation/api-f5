from django.utils.html import strip_tags
from django.db import transaction

from f5.models.Permission.Permission import Permission

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException
from f5.helpers.Database import Database as DBHelper
from django.db import connection



class IdentityGroup:
    def __init__(self, identityGroupIdentifier: str,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.identityGroupIdentifier = identityGroupIdentifier



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        c = connection.cursor()

        try:
            c.execute("SELECT * FROM identity_group WHERE identity_group_identifier = %s", [
                self.identityGroupIdentifier
            ])

            return DBHelper.asDict(c)[0]

        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    def modify(self, data: dict) -> None:
        sql = ""
        values = []
        roles = dict()

        c = connection.cursor()
        if self.__exists():
            for k, v in data.items():
                if any(exc in k for exc in (
                        "roles_partition",
                )):
                    # "roles_partition": {
                    #     "staff": [
                    #         {
                    #             "assetId": 1,
                    #             "partition": "any"
                    #         }
                    #     ],
                    #  "nonExistent": []
                    # }

                    if isinstance(v, dict):
                        for rk, rv in v.items():
                            roles[rk] = rv
                else:
                    sql += k + "=%s,"
                    values.append(strip_tags(v))  # no HTML allowed.

            try:
                with transaction.atomic():
                    identityGroupId = self.info()["id"]

                    # Patch identity group.
                    c.execute("UPDATE identity_group SET "+sql[:-1]+" WHERE id = "+str(identityGroupId),
                        values
                    )

                    # Replace associated roles with roles[]' elements.
                    try:
                        # Empty existent roles.
                        Permission.cleanup(identityGroupId)
                    except Exception:
                        pass

                    for roleName, partitionsAssetsList in roles.items():
                        for partitionsAssetDict in partitionsAssetsList:
                            try:
                                Permission.add(identityGroupId, roleName, partitionsAssetDict["assetId"], partitionsAssetDict["partition"])
                            except Exception:
                                pass

            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        else:
            raise CustomException(status=404, payload={"database": {"message": "Non existent identity group"}})



    def delete(self) -> None:
        c = connection.cursor()

        if self.__exists():
            try:
                c.execute("DELETE FROM identity_group WHERE identity_group_identifier = %s", [
                    self.identityGroupIdentifier
                ])

                # Foreign keys' on cascade rules will clean the linked items on db.

            except Exception as e:
                raise CustomException(status=400, payload={"database": e.__str__()})
            finally:
                c.close()

        else:
            raise CustomException(status=404, payload={"database": {"message": "Non existent identity group"}})



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(showPrivileges: bool = False) -> dict:
        # List identity groups with related information regarding the associated roles on partitions
        # and optionally detailed privileges' descriptions.

        j = 0
        c = connection.cursor()

        try:
            c.execute("SELECT "
                "identity_group.*, " 

                "IFNULL(GROUP_CONCAT( "
                    "DISTINCT CONCAT(role.role,'::',CONCAT(partition.id_asset,'::',partition.partition)) " 
                    "ORDER BY role.id "
                    "SEPARATOR ',' "
                "), '') AS roles_partition, "

                "IFNULL(GROUP_CONCAT( "
                    "DISTINCT CONCAT(privilege.privilege,'::',partition.id_asset,'::',partition.partition,'::',privilege.propagate_to_all_asset_partitions,'::',privilege.propagate_to_all_assets) " 
                    "ORDER BY privilege.id "
                    "SEPARATOR ',' "
                "), '') AS privileges_partition "

                "FROM identity_group "
                "LEFT JOIN group_role_partition ON group_role_partition.id_group = identity_group.id "
                "LEFT JOIN role ON role.id = group_role_partition.id_role "
                "LEFT JOIN `partition` ON `partition`.id = group_role_partition.id_partition "
                "LEFT JOIN role_privilege ON role_privilege.id_role = role.id "
                "LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege "
                "GROUP BY identity_group.id"
            )

            # Simple start query:
            # SELECT identity_group.*, role.role, privilege.privilege, `partition`.partition
            # FROM identity_group
            # LEFT JOIN group_role_partition ON group_role_partition.id_group = identity_group.id
            # LEFT JOIN role ON role.id = group_role_partition.id_role
            # LEFT JOIN `partition` ON `partition`.id = group_role_partition.id_partition
            # LEFT JOIN role_privilege ON role_privilege.id_role = role.id
            # LEFT JOIN privilege ON privilege.id = role_privilege.id_privilege
            # GROUP BY identity_group.id

            items = DBHelper.asDict(c)

            # "items": [
            # ...,
            # {
            #    "id": 2,
            #    "name": "groupStaff",
            #    "identity_group_identifier": "cn=groupStaff,cn=users,dc=lab,dc=local",
            #    "roles_partition": "staff::1::Common",
            #    "privileges_partition": "certificates_post::1::Common::1::0,poolMember_get::1::Common::0::0,poolMember_patch::1::Common::0::0,poolMembers_get::1::Common::0::0,poolMemberStats_get::1::Common::0::0,pools_get::1::Common::0::0,partitions_get::1::Common::1::1"
            # },
            # ...
            # ]

            for ln in items:
                if "roles_partition" in items[j]:
                    if "," in ln["roles_partition"]:
                        items[j]["roles_partition"] = ln["roles_partition"].split(",") # "staff::1::partition,...,readonly::2::partition" string to list value: replace into original data structure.
                    else:
                        items[j]["roles_partition"] = [ ln["roles_partition"] ] # simple string to list.

                    # "roles_partition": [
                    #    "admin::1::any",
                    #    "staff::1::PARTITION1",
                    #    "staff::2::PARTITION2"
                    # ]

                    rolesStructure = dict()
                    for rls in items[j]["roles_partition"]:
                        if "::" in rls:
                            rlsList = rls.split("::")
                            if not str(rlsList[0]) in rolesStructure:
                                # Initialize list if not already done.
                                rolesStructure[rlsList[0]] = list()

                            rolesStructure[rlsList[0]].append({
                                "assetId": rlsList[1],
                                "partition": rlsList[2]
                            })

                    items[j]["roles_partition"] = rolesStructure

                    #"roles_partition": {
                    #    "staff": [
                    #        {
                    #            "assetId": 1
                    #            "partition": "PARTITION1"
                    #        },
                    #        {
                    #            "assetId": 2
                    #            "partition": "PARTITION2"
                    #        },
                    #    ],
                    #    "admin": [
                    #        {
                    #            "assetId": 1
                    #            "partition": "any"
                    #        },
                    #    ]
                    #}

                if showPrivileges:
                    # Add detailed privileges' descriptions to the output.
                    if "privileges_partition" in items[j]:
                        if "," in ln["privileges_partition"]:
                            items[j]["privileges_partition"] = ln["privileges_partition"].split(",")
                        else:
                            items[j]["privileges_partition"] = [ ln["privileges_partition"] ]

                        ppStructure = dict()
                        for pls in items[j]["privileges_partition"]:
                            if "::" in pls:
                                pList = pls.split("::")
                                if not str(pList[0]) in ppStructure:
                                    ppStructure[pList[0]] = list()

                                # If propagate_to_all_asset_partitions is set, set "any" for partitions value.
                                # It means that a privilege does not require the partitions to be specified <--> it's valid for all partitions within the asset.
                                if pList[3]:
                                    if int(pList[3]):
                                        pList[2] = "any"

                                # If propagate_to_all_assets is set, set "any" for assets value.
                                # It means that a privilege does not require the asset to be specified <--> it's valid for all assets.
                                if pList[4]:
                                    if int(pList[4]):
                                        pList[1] = 0
                                        pList[2] = "any"

                                if not any(v['assetId'] == 0 for v in ppStructure[pList[0]]): # insert value only if not already present (applied to assetId "0").
                                    ppStructure[pList[0]].append({
                                        "assetId": pList[1],
                                        "partition": pList[2],
                                    })

                        items[j]["privileges_partition"] = ppStructure
                else:
                    del items[j]["privileges_partition"]

                j = j+1

            return dict({
                "items": items
            })

        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    @staticmethod
    def add(data: dict) -> None:
        s = ""
        keys = "("
        values = []
        roles = dict()

        c = connection.cursor()

        # Build SQL query according to dict fields (only whitelisted fields pass).
        for k, v in data.items():
            # roles is a dictionary of related roles/partitions, which is POSTed together with the main identity group item.
            if any(exc in k for exc in (
                    "roles_partition",
            )):
                # "roles_partition": {
                #     "staff": [
                #         {
                #             "assetId": 1,
                #             "partition": "any"
                #         }
                #     ],
                #  "nonExistent": []
                # }

                if isinstance(v, dict):
                    for rk, rv in v.items():
                        roles[rk] = rv
            else:
                s += "%s,"
                keys += k + ","
                values.append(strip_tags(v))  # no HTML allowed.

        keys = keys[:-1]+")"

        try:
            with transaction.atomic():
                # Insert identity group.
                c.execute("INSERT INTO identity_group "+keys+" VALUES ("+s[:-1]+")",
                    values
                )
                igId = c.lastrowid

                # Add associated roles (no error on non-existent role).
                for roleName, partitionsAssetsList in roles.items():
                    for partitionsAssetDict in partitionsAssetsList:
                        try:
                            Permission.add(igId, roleName, partitionsAssetDict["assetId"], partitionsAssetDict["partition"])
                        except Exception:
                            pass

        except Exception as e:
            raise CustomException(status=400, payload={"database": e.__str__()})
        finally:
            c.close()



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __exists(self) -> int:
        c = connection.cursor()
        try:
            c.execute("SELECT COUNT(*) AS c FROM identity_group WHERE identity_group_identifier = %s", [
                self.identityGroupIdentifier
            ])
            o = DBHelper.asDict(c)

            return int(o[0]['c'])

        except Exception:
            return 0
        finally:
            c.close()
