from __future__ import annotations
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

PolicyRuleData: Dict[str, Union[str, list]] = {
    "name": "",
    "actions": [],
    "conditions": []
}


class Policy:
    def __init__(self, assetId: int, partitionName: str, policyName: str, subPath: str = "", loadRules: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.partition: str = partitionName
        self.subPath: str = subPath
        self.name: str = policyName
        self.fullPath: str = ""
        self.generation: int = 0
        self.selfLink: str = ""
        self.lastModified: str = ""
        self.status: str = ""
        self.strategy: str = ""
        self.strategyReference: Link
        self.rulesReference: RulesReference

        self.rules: List[PolicyRuleData] = []

        self.__load(loadRules=loadRules)



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def repr(self):
        return Misc.deepRepr(self)



    def modify(self, data):
        try:
            Backend.modify(self.assetId, self.partition, self.name, data, self.subPath)

            for k, v in Misc.toDict(data).items():
                setattr(self, k, v)
        except Exception as e:
            raise e



    def delete(self):
        try:
            Backend.delete(self.assetId, self.partition,  self.name, self.subPath)
            del self
        except Exception as e:
            raise e



    def getRulesData(self) -> List[dict]:
        try:
            return Backend.rules(self.assetId, self.partition, self.name, self.subPath)
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int, partitionName: str, subPath: str = "", loadRules: bool = False) -> List[Policy]:
        import threading
        l = []

        def loadPolicy(a, p, n, s, lr, o):
            o.append(Policy(a, p, n, s, lr)) # append Policy object.

        try:
            summary = Backend.list(assetId, partitionName)
            workers = [threading.Thread(target=loadPolicy, args=(assetId, partitionName, el.get("name", ""), subPath, loadRules, l)) for el in summary]
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
            from f5.helpers.Log import Log
            data = Backend.info(self.assetId, self.partition, self.name, self.subPath)
            if data:
                for k, v in data.items():
                    setattr(self, k, v)

                if loadRules:
                    self.rules = self.getRulesData()
                else:
                    del self.rules
            else:
                raise CustomException(status=404)
        except Exception as e:
            raise e
