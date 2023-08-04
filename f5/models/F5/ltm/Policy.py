from typing import List, Dict, Union

from f5.models.F5.ltm.backend.Policy import Policy as Backend

from f5.helpers.Exception import CustomException
from f5.helpers.Misc import Misc


Link: Dict[str, str] = {
    "link": ""
}

RulesReference: Dict[str, Union[str, bool]] = {
    "link": "",
    "isSubcollection": False
}

class Policy:
    def __init__(self, assetId: int, partitionName: str, policySubPath: str, policyName: str, loadRules: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.partition: str = partitionName
        self.subPath: str = policySubPath
        self.name: str = policyName
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.lastModified: str = ""
        self.status: str = ""
        self.strategy: str = ""
        self.strategyReference: Link
        self.rulesReference: RulesReference

        self.rules: List[dict] = []

        self.__load(loadRules=loadRules)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        return Misc.deepRepr(self)



    def modify(self, data):
        try:
            Backend.modify(self.assetId, self.partition, self.subPath, self.name, data)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Backend.delete(self.assetId, self.partition, self.subPath, self.name)
            del self
        except Exception as e:
            raise e



    def getRulesData(self) -> List[dict]:
        try:
            return Backend.rules(self.assetId, self.partition, self.subPath, self.name)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def dataList(assetId: int, partitionName: str, policySubPath: str = "", loadRules: bool = False) -> List[dict]:
        import threading

        def loadData(a, p, s, o):
            o["assetId"] = assetId

            if loadRules:
                try:
                    o["rules"] = Backend.rules(a, p, s, o["name"])
                except CustomException as ex:
                    if ex.status == 404:
                        o["rules"] = []
                    else:
                        raise ex

        try:
            l = Backend.list(assetId, partitionName)
            workers = [threading.Thread(target=loadData, args=(assetId, partitionName, policySubPath, el)) for el in l]
            for w in workers:
                w.start()
            for w in workers:
                w.join()

            return l
        except Exception as e:
            raise e



    @staticmethod
    def add(assetId: int, data: dict) -> None:
        try:
            Backend.add(assetId, data)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __load(self, loadRules: bool = False) -> None:
        try:
            data = Backend.info(self.assetId, self.partition, self.subPath, self.name)
            if data:
                if loadRules:
                    data["rules"] = self.getRulesData()

                for k, v in data.items():
                    setattr(self, k, v)
            else:
                raise CustomException(status=404)
        except Exception as e:
            raise e
