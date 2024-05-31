from f5.models.F5.ltm.Node import Node
from f5.models.F5.ltm.Pool import Pool
from f5.models.F5.ltm.PoolMember import PoolMember
from f5.models.History.History import History

from f5.helpers.Log import Log


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
            self.__removePoolsMembership(poolName)
            self.__deleteNode()

        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __findPoolName(self) -> list:
        membership = list()

        try:
            poolList = Pool.dataList(self.assetId, self.partitionName)
            for pool in poolList:
                members = Pool(self.assetId, self.partitionName, pool["name"], pool.get("subPath", "")).getMembersData()
                for member in members:
                    if self.nodeName == member["name"].split(":")[0]:
                        membership.append( (pool["name"], member["name"]) )

            return membership
        except Exception as e:
            raise e



    def __removePoolsMembership(self, membership: list) -> None:
        try:
            for member in membership:
                Log.actionLog("Node deletion workflow: attempting to remove node " + str(member[1]) + " from pool " + str(member[0]))
                PoolMember(self.assetId, member[0], self.partitionName, member[1]).delete()
                self.__logDeletedObjects(member[0], "pool", "removing from pool", "removed")

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
        self.__logDeletedObjects(self.nodeName, "node", "deletion", "deleted")



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
