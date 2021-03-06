from f5.models.Permission.repository.IdentityGroup import IdentityGroup as Repository


class IdentityGroup:
    def __init__(self, identityGroupIdentifier: str,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = 0
        self.identity_group_identifier = identityGroupIdentifier
        self.name = ""



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            return Repository.get(self.identity_group_identifier)
        except Exception as e:
            raise e



    def modify(self, data: dict) -> None:
        try:
            Repository.modify(self.identity_group_identifier, data)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository.delete(self.identity_group_identifier)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list() -> list:
        try:
            return Repository.list()
        except Exception as e:
            raise e



    @staticmethod
    def listWithRelated(showPrivileges: bool = False) -> list:
        # List identity groups with related information regarding the associated roles on partitions
        # and optionally detailed privileges' descriptions.
        j = 0

        try:
            items = Repository.list()

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

                                # Differentiate permission type:
                                # global:
                                #     a privilege does not require the asset to be specified <--> it's valid for all assets;
                                #     set "any" for assets value.

                                # asset:
                                #    a privilege does not require the partitions to be specified <--> it's valid for all partitions within the asset;
                                #    set "any" for partitions value.
                                #
                                # object:
                                #     standard.

                                if pList[3]:
                                    if pList[3] == "global":
                                        pList[1] = 0
                                        pList[2] = "any"
                                    if pList[3] == "asset":
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

            return items
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> None:
        try:
            Repository.add(data)
        except Exception as e:
            raise e
