from f5.models.F5.Node import Node
from f5.models.F5.Pool import Pool
from f5.models.F5.PoolMember import PoolMember
from f5.models.History.History import History

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException


class DeleteNodeWorkflow:
    def __init__(self, assetId: int, partitionName: str, nodeNmae: str, user: dict):
        self.assetId = assetId
        self.partitionName = partitionName
        self.nodeName = nodeNmae
        self.username = user["username"]
        self.pool = ""



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self) -> None:
        try:
            poolName = self.__findPoolName()
            Log.log(poolName, 'PPPPPPPPPPPPP')
            self.__removePoolMember(poolName)
            self.__deleteNode()

        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __findPoolName(self) -> str:
        try:
            poolList = Pool.list(self.assetId, self.partitionName)
            for pool in poolList:
                members = Pool(self.assetId, self.partitionName, pool["name"]).members()
                if self.nodeName in [ member["name" ].split(":")[0] for member in members ]: # drop the port info from the name field to match self.nodeName.
                    return pool["name"]

            return ""
        except Exception as e:
            raise e



    def __removePoolMember(self, poolName: str) -> None:
        Log.actionLog("Node deletion workflow: attempting to remove node " + self.nodeName + " from pool " + poolName)

        try:
            PoolMember(self.assetId, poolName, self.partitionName, self.nodeName).delete()
        except Exception as e:
            raise e



    def __deleteNode(self) -> None:
        Log.actionLog("Node deletion workflow: attempting to delete node: " + self.nodeName)

        try:
            node = Node(self.assetId, self.partitionName, self.nodeName)
            node.delete()

        except Exception as e:
            if e.__class__.__name__ == "CustomException":
                if "F5" in e.payload and e.status == 400 and "is referenced" in e.payload["F5"]:
                    Log.log("Node " + self.nodeName + " in use; not deleting it. ")
                else:
                    Log.log("[ERROR] Node deletion workflow: cannot delete node " + self.nodeName + ": " + str(e.payload))
            else:
                Log.log("[ERROR] Node deletion workflow: cannot delete node " + self.nodeName + ": " + e.__str__())

        Log.actionLog("Deleted node: " + self.nodeName)



    def __logDeletedObjects(self) -> None:
        try:
            History.add({
                "username": self.username,
                "action": "[WORKFLOW] " + self.nodeName + " deletion",
                "asset_id": self.assetId,
                "config_object_type": "node",
                "config_object": "/"+self.partitionName+"/" +  self.nodeName,
                "status": "deleted"
            })
        except Exception:
            pass
