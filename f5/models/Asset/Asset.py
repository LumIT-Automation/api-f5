from f5.models.Asset.repository.Asset import Asset as Repository

from f5.helpers.Misc import Misc


class Asset:
    def __init__(self, assetId: int, showPassword: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = int(assetId)
        self.fqdn: str = ""
        self.protocol: str = "https"
        self.port: int = 443
        self.path: str = "/"
        self.tlsverify: bool = True
        self.baseurl: str = ""
        self.datacenter: str = ""
        self.environment: str = ""
        self.position: str = ""
        self.username: str = ""
        self.password: str = ""

        self.__load(showPassword=showPassword)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        from f5.helpers.Log import Log
        return Misc.deepRepr(self)



    def modify(self, data: dict) -> None:
        try:
            Repository.modify(self.id, data)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self) -> None:
        try:
            Repository.delete(self.id)
            del self
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def dataList(showPassword: bool = False, filter: dict = None) -> list:
        filter = filter or {}

        try:
            return Repository.list(showPassword=showPassword, filter=filter)
        except Exception as e:
            raise e



    @staticmethod
    def add(data: dict) -> None:
        from f5.models.Permission.Partition import Partition as PermissionPartition

        try:
            aId = Repository.add(data)

            # When inserting an asset, add the "any" partition (Permission).
            PermissionPartition.add(aId, "any")
        except Exception as e:
            raise e



    @staticmethod
    def purgeAll() -> None:
        from f5.models.Permission.Partition import Partition

        try:
            Partition.purgeAll()
            Repository.purgeAll()
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self, showPassword: bool) -> None:
        try:
            data = Repository.get(self.id, showPassword=showPassword)
            for k, v in data.items():
                setattr(self, k, v)

            if not showPassword:
                del self.username
                del self.password

        except Exception as e:
            raise e
