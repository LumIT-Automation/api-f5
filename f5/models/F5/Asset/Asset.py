from f5.models.F5.Asset.repository.Asset import Asset as Repository


class Asset:
    def __init__(self, assetId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = int(assetId)
        self.address = ""
        self.fqdn = ""
        self.baseurl = ""
        self.tlsverify = ""
        self.datacenter = ""
        self.environment = ""
        self.position = ""

        self.username = ""
        self.password = ""



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def load(self) -> None:
        try:
            data = Repository.get(self.id)
            for k, v in data.items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def info(self) -> dict:
        try:
            info = Repository.get(self.id)
            return info
        except Exception as e:
            raise e



    def modify(self, data: dict) -> None:
        try:
            Repository.modify(self.id, data)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository.delete(self.id)
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
    def add(data: dict) -> None:
        try:
            aid = Repository.add(data)

            # When inserting an asset, add the "any" partition (Permission).
            from f5.models.Permission.Partition import Partition as PermissionPartition
            PermissionPartition.add(aid, "any")
        except Exception as e:
            raise e
