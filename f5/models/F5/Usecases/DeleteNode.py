import re

from f5.models.F5.ltm.Node import Node
from f5.models.F5.ltm.Pool import Pool
from f5.models.F5.ltm.PoolMember import PoolMember
from f5.models.History.History import History

from f5.helpers.Log import Log


class DeleteNodeWorkflow:
    def __init__(self, assetId: int, partitionName: str, nodeNmae: str, user: dict, subPath: str = ""):
        self.assetId = assetId
        self.partitionName = partitionName
        self.nodeName = nodeNmae
        self.subPath = subPath
        self.username = user["username"]
        self.pool = ""



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self) -> None:
        Log.actionLog("Node deletion workflow: attempting to delete node: " + self.nodeName)
        deleted = False
        while not deleted:
            try:
                Node(self.assetId, self.partitionName, self.nodeName, self.subPath).delete()
                deleted = True

            except Exception as e:
                if e.__class__.__name__ == "CustomException" and e.status == 400 and " is referenced by a member of pool" in e.payload.get("F5", {}):
                    pool = DeleteNodeWorkflow.__findReferencedPool(e.payload)
                    nodePort = self.__getNodePort(pool)
                    if nodePort:
                        self.__removeFromPool(pool, nodePort)
                    else:
                        raise e
                else:
                    raise e

        Log.actionLog("Deleted node: " + self.nodeName)
        self.__logDeletedObjects(self.nodeName, "node", "deletion", "deleted")



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __removeFromPool(self, poolData: dict, nodePort: int) -> None:
        try:
            Log.actionLog("Node deletion workflow: attempting to remove node " + self.nodeName + " from pool " + poolData["name"])
            PoolMember(self.assetId, poolData["name"], self.partitionName, self.nodeName+":"+str(nodePort), poolData["subPath"], self.subPath).delete()
            self.__logDeletedObjects(poolData["name"], "pool", "removing from pool", "removed")

        except Exception as e:
            raise e



    def __getNodePort(self, poolData: dict) -> int:
        nodePort = 0

        try:
            nodeList = PoolMember.dataList(self.assetId, self.partitionName, poolData["name"], poolData["subPath"])
            for n in nodeList:
                if n.get("name", "").split(":")[0] == self.nodeName:
                    nodePort = n.get("name", "").split(":")[1]

            return nodePort
        except Exception as e:
            raise e



    def __logDeletedObjects(self, object: str, object_type: str, action: str, status: str) -> None:
            try:
                History.add({
                    "username": self.username,
                    "action": "[WORKFLOW] " + self.nodeName + " " + action,
                    "asset_id": self.assetId,
                    "config_object_type": object_type,
                    "config_object": "/"+self.partitionName+"/" +  object,
                    "status": status
                })
            except Exception:
                pass



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __findReferencedPool(ePayload: dict) -> dict:
        pool = {
            "name": "",
            "partition": "",
            "subPath": ""
        }

        try:
            messageString = ePayload.get("F5", "")
            if messageString:
                match = re.search(r'by a member of pool (?=\')([^.]+)\.?', messageString)
                poolPathList = match.group(1).replace("'", "").split('/')
                poolPathList = list(filter(bool, poolPathList)) # remove the leading element "".

                pool["name"] = poolPathList.pop(-1)
                pool["subPath"] =  '/'.join(poolPathList[1:])
                pool["partition"] = poolPathList[0]

            return pool
        except Exception as e:
            raise e
