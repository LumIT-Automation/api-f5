from collections import OrderedDict

from f5.models.F5.Node import Node
from f5.models.F5.Monitor import Monitor
from f5.models.F5.Pool import Pool
from f5.models.F5.SnatPool import SnatPool
from f5.models.F5.PoolMember import PoolMember
from f5.models.F5.Profile import Profile
from f5.models.F5.VirtualServer import VirtualServer
from f5.models.History import History

from f5.helpers.Log import Log



class VirtualServersWorkflow:
    def __init__(self, assetId: int, partitionName: str, data: dict, user: dict):
        self.assetId = assetId
        self.partitionName = partitionName
        self.data = data
        self.username = user["username"]
        self.routeDomain = ""

        if "routeDomainId" in data["virtualServer"]:
            self.routeDomain = "%"+str(data["virtualServer"]["routeDomainId"]) # %1.

        self.__createdObjects = {
            "node": [],
            "monitor": {},
            "pool": {},
            "poolMember": [],
            "profiles": [],
            "snatPool": {},
            "virtualServer": {}
        }

        self.__usedObjects = {
            "node": [],
            "monitor": {},
            "pool": {},
            "poolMember": [],
            "profiles": [],
            "snatPool": {},
            "virtualServer": {}
        }



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def add(self) -> None:
        vsType = self.data["virtualServer"]["type"]
        # Performance Layer 4/7.
        self.__createNodes()
        self.__createMonitor()
        self.__createPool()
        self.__createPoolMembers()
        self.__createProfiles()
        self.__createVirtualServer()

        self.__logCreatedObjects()



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def relatedF5Objects() -> list:
        return ["node", "monitor", "pool", "poolMember", "profile", "virtualServer"]



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __createNodes(self) -> None:
        for el in self.data["pool"]["nodes"]:
            nodeName = el["name"]
            nodeAddress = el["address"]

            try:
                Log.actionLog("Virtual server workflow: attempting to create node: "+str(nodeAddress))

                Node.add(self.assetId, {
                    "name": nodeName,
                    "address": nodeAddress+self.routeDomain,
                    "partition": self.partitionName,
                    "State": "up"
                })

                # Keep track of CREATED nodes.
                self.__createdObjects["node"].append({
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": nodeName,
                    "address": nodeAddress+self.routeDomain,
                })

            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 409 and "already exists" in e.payload["F5"]:
                        Log.log("Node "+str(nodeName)+"/"+str(nodeAddress)+" already exists with the same/address name; using it. ")

                        # Keep track of USED node.
                        self.__usedObjects["node"].append({
                            "asset": self.assetId,
                            "partition": self.partitionName,
                            "name": nodeName,
                            "address": nodeAddress+self.routeDomain,
                        })
                    else:
                        self.__cleanCreatedObjects()
                        raise e
                else:
                    self.__cleanCreatedObjects()
                    raise e

        Log.actionLog("Created objects: "+str(self.__createdObjects))
        Log.actionLog("Reused existent objects: "+str(self.__usedObjects))



    def __createMonitor(self) -> None:
        monitorName = self.data["monitor"]["name"]
        monitorType = self.data["monitor"]["type"]

        try:
            Log.actionLog("Virtual server workflow: attempting to create monitor: "+str(monitorName))

            mData = {
                "name": monitorName,
                "partition": self.partitionName
            }

            if "send" in self.data["monitor"]:
                mData["send"] = self.data["monitor"]["send"]
            if "recv" in self.data["monitor"]:
                mData["recv"] = self.data["monitor"]["recv"]

            Monitor.add(self.assetId, monitorType, mData)

            # Keep track of CREATED monitor.
            self.__createdObjects["monitor"] = {
                "asset": self.assetId,
                "partition": self.partitionName,
                "name": monitorName,
                "type": monitorType
            }

        except Exception as e:
            if e.__class__.__name__ == "CustomException":
                if "F5" in e.payload and e.status == 409 and "already exists" in e.payload["F5"]:
                    Log.log("Monitor "+str(monitorName)+" already exists with the same name; using it. ")

                    # Keep track of USED monitor.
                    self.__usedObjects["monitor"] = {
                        "asset": self.assetId,
                        "partition": self.partitionName,
                        "name": monitorName,
                        "type": monitorType
                    }
                else:
                    self.__cleanCreatedObjects()
                    raise e
            else:
                self.__cleanCreatedObjects()
                raise e

        Log.actionLog("Created objects: "+str(self.__createdObjects))
        Log.actionLog("Reused existent objects: "+str(self.__usedObjects))



    def __createPool(self) -> None:
        poolName = self.data["pool"]["name"]

        try:
            Log.actionLog("Virtual server workflow: attempting to create pool: "+str(poolName))

            Pool.add(self.assetId, {
                "name": poolName,
                "partition": self.partitionName,
                "monitor": "/"+self.partitionName+"/"+self.data["monitor"]["name"],
                "loadBalancingMode": self.data["pool"]["loadBalancingMode"]
            })

            # Keep track of CREATED pool.
            self.__createdObjects["pool"] = {
                "asset": self.assetId,
                "partition": self.partitionName,
                "name": poolName
            }

        except Exception as e:
            if e.__class__.__name__ == "CustomException":
                if "F5" in e.payload and e.status == 409 and "already exists" in e.payload["F5"]:
                    Log.log("Pool "+str(poolName)+" already exists with the same name; using it. ")

                    # Keep track of USED pool.
                    self.__usedObjects["pool"] = {
                        "asset": self.assetId,
                        "partition": self.partitionName,
                        "name": poolName
                    }
                else:
                    self.__cleanCreatedObjects()
                    raise e
            else:
                self.__cleanCreatedObjects()
                raise e

        Log.actionLog("Created objects: "+str(self.__createdObjects))
        Log.actionLog("Reused existent objects: "+str(self.__usedObjects))



    def __createPoolMembers(self) -> None:
        poolName = self.data["pool"]["name"]

        for el in self.data["pool"]["nodes"]:
            nodeName = el["name"]
            poolMemberPort = el["port"]
            poolMemberName = nodeName+":"+str(poolMemberPort)

            try:
                Log.actionLog("Virtual server workflow: attempting to create pool members: associate "+str(nodeName)+" to "+str(poolName)+" on port "+str(poolMemberPort))

                PoolMember.add(self.assetId, self.partitionName, poolName, {
                        "name": poolMemberName,
                        "State": "up",
                        "session": "user-enabled"
                    }
                )

                # Keep track of CREATED pool members.
                self.__createdObjects["poolMember"].append({
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "pool": poolName,
                    "name": poolMemberName
                })

            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 409 and "already exists" in e.payload["F5"]:
                        Log.log("Pool member "+str(poolMemberName)+" already exists; using it. ")

                        # Keep track of USED node.
                        self.__usedObjects["poolMember"].append({
                            "asset": self.assetId,
                            "partition": self.partitionName,
                            "pool": poolName,
                            "name": poolMemberName
                        })
                    else:
                        self.__cleanCreatedObjects()
                        raise e
                else:
                    self.__cleanCreatedObjects()
                    raise e

        Log.actionLog("Created objects: "+str(self.__createdObjects))
        Log.actionLog("Reused existent objects: "+str(self.__usedObjects))



    def __createProfiles(self) -> None:
        for el in self.data["profiles"]:
            profileName = el["name"]
            profileType = el["type"]

            postData = {
                "name": profileName,
                "partition": self.partitionName
            }

            # Additional POST data.
            if "idleTimeout" in el:
                postData["idleTimeout"] = el["idleTimeout"]
            if "defaultsFrom" in el:
                postData["defaultsFrom"] = el["defaultsFrom"]

            if "cert" in el:
                postData["cert"] = el["cert"]
            if "key" in el:
                postData["key"] = el["key"]
            if "chain" in el:
                postData["chain"] = el["chain"]

            try:
                Log.actionLog("Virtual server workflow: attempting to create profile: "+str(profileName))

                Profile.add(self.assetId, profileType, postData)

                # Keep track of CREATED profile.
                self.__createdObjects["profiles"].append({
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": profileName,
                    "type": profileType
                })

            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 409 and "already exists" in e.payload["F5"]:
                        Log.log("Profile "+str(profileName)+" already exists with the same name; using it. ")

                        # Keep track of USED pool.
                        self.__usedObjects["profiles"].append({
                            "asset": self.assetId,
                            "partition": self.partitionName,
                            "name": profileName,
                            "type": profileType
                        })
                    else:
                        self.__cleanCreatedObjects()
                        raise e
                else:
                    self.__cleanCreatedObjects()
                    raise e

        Log.actionLog("Created objects: "+str(self.__createdObjects))
        Log.actionLog("Reused existent objects: "+str(self.__usedObjects))



    def __createSnatPool(self) -> None:
        snatPoolName = self.data["snatPool"]["name"]

        try:
            Log.actionLog("Virtual server workflow: attempting to create SNAT pool: snatPool_"+str(snatPoolName))

            SnatPool.add(self.assetId, {
                "name": snatPoolName,
                "partition": self.partitionName,
                "monitor": "/"+self.partitionName+"/"+self.data["monitor"]["name"],
                "members": [
                    "/"+self.partitionName+"/"+self.data["snatPool"]["snatIPAddress"]+self.routeDomain
                ]
            })

            # Keep track of CREATED snatPool.
            self.__createdObjects["snatPool"] = {
                "asset": self.assetId,
                "partition": self.partitionName,
                "name": snatPoolName
            }

        except Exception as e:
            if e.__class__.__name__ == "CustomException":
                if "F5" in e.payload and e.status == 409 and "already exists" in e.payload["F5"]:
                    Log.log("Snat pool "+str(snatPoolName)+" already exists with the same name; using it. ")

                    # Keep track of USED snatPool.
                    self.__usedObjects["snatPool"] = {
                        "asset": self.assetId,
                        "partition": self.partitionName,
                        "name": snatPoolName
                    }
                else:
                    self.__cleanCreatedObjects()
                    raise e
            else:
                self.__cleanCreatedObjects()
                raise e

        Log.actionLog("Created objects: "+str(self.__createdObjects))
        Log.actionLog("Reused existent objects: "+str(self.__usedObjects))



    def __createVirtualServer(self) -> None:
        profiles = list()
        virtualServerName = self.data["virtualServer"]["name"]
        virtualServerDestination = self.data["virtualServer"]["destination"]
        virtualServerMask = self.data["virtualServer"]["mask"]
        virtualServerSource = self.data["virtualServer"]["source"]
        virtualServerSnat = self.data["virtualServer"]["snat"]

        if self.routeDomain:
            i, m = virtualServerSource.split("/")
            virtualServerSource = i+self.routeDomain+"/"+m

            i, p = virtualServerDestination.split(":")
            virtualServerDestination = i+self.routeDomain+":"+p

        try:
            Log.actionLog("Virtual server workflow: attempting to create virtual server: "+str(virtualServerName))

            for el in self.data["profiles"]:
                context = "all"
                if "context" in el:
                    context = el["context"]

                profiles.append({
                    "name": "/"+self.partitionName+"/"+el["name"],
                    "context": context
                })

            VirtualServer.add(self.assetId, {
                "name": virtualServerName,
                "partition": self.partitionName,
                "destination": "/"+self.partitionName+"/"+virtualServerDestination,
                "ipProtocol": "tcp",
                "profiles": profiles,
                "mask": virtualServerMask,
                "pool":  "/"+self.partitionName+"/"+self.data["pool"]["name"],
                "source": virtualServerSource,
                "sourceAddressTranslation": {
                    "type": virtualServerSnat
                }
            })

            # Keep track of CREATED virtual server.
            self.__createdObjects["virtualServer"] = {
                "asset": self.assetId,
                "partition": self.partitionName,
                "name": virtualServerName
            }

        except Exception as e:
            if e.__class__.__name__ == "CustomException":
                if "F5" in e.payload and e.status == 409 and "already exists" in e.payload["F5"]:
                    Log.log("virtual server "+str(virtualServerName)+" already exists with the same name; using it. ")

                    # Keep track of USED virtual server.
                    self.__usedObjects["virtualServer"] = {
                        "asset": self.assetId,
                        "partition": self.partitionName,
                        "name": virtualServerName
                    }
                else:
                    self.__cleanCreatedObjects()
                    raise e
            else:
                self.__cleanCreatedObjects()
                raise e

        Log.actionLog("Created objects: "+str(self.__createdObjects))
        Log.actionLog("Reused existent objects: "+str(self.__usedObjects))


    
    def __cleanCreatedObjects(self):
        Log.log("Virtual server workflow: cleanup")

        # Reverse elements in order to delete from leaf to branch.
        self.__createdObjects = OrderedDict(reversed(list(self.__createdObjects.items())))

        for k, v in self.__createdObjects.items():
            if k == "virtualServer":
                if "name" in v:
                    virtualServerName = v["name"]
                    try:
                        Log.log("Virtual server workflow: cleanup virtualServer "+virtualServerName)

                        vs = VirtualServer(self.assetId, self.partitionName, virtualServerName)
                        vs.delete()
                    except Exception:
                        # If deletion failed, log.
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+virtualServerName)

            if k == "profiles":
                for n in v:
                    profileName = n["name"]
                    profileType = n["type"]
                    try:
                        Log.log("Virtual server workflow: cleanup profile "+profileName)

                        profile = Profile(self.assetId, self.partitionName, profileType, profileName)
                        profile.delete()
                    except Exception:
                        # If deletion failed, log.
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+profileName)

            if k == "poolMember":
                for n in v:
                    poolMemberName = n["name"]
                    poolName = n["pool"]
                    try:
                        Log.log("Virtual server workflow: cleanup pool member "+poolMemberName)

                        poolMember = PoolMember(self.assetId, poolName, self.partitionName, poolMemberName)
                        poolMember.delete()
                    except Exception:
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+poolMemberName)

            if k == "pool":
                if "name" in v:
                    poolName = v["name"]
                    try:
                        Log.log("Virtual server workflow: cleanup pool "+poolName)

                        pool = Pool(self.assetId, self.partitionName, poolName)
                        pool.delete()
                    except Exception:
                        # If deletion failed, log.
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+poolName)

            if k == "monitor":
                if "name" in v:
                    monitorName = v["name"]
                    monitorType = v["type"]
                    try:
                        Log.log("Virtual server workflow: cleanup monitor "+monitorName)

                        monitor = Monitor(self.assetId, self.partitionName, monitorType, monitorName)
                        monitor.delete()
                    except Exception:
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+monitorName)

            if k == "node":
                for n in v:
                    nodeName = n["name"]
                    try:
                        Log.log("Virtual server workflow: cleanup node "+nodeName)

                        node = Node(self.assetId, self.partitionName, nodeName)
                        node.delete()
                    except Exception:
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+nodeName)



    def __logCreatedObjects(self) -> None:
        for k, v in self.__createdObjects.items():
            try:
                if any(key in k for key in ("virtualServer", "pool", "monitor")):
                    if "name" in v:
                        History.add({
                            "username": self.username,
                            "action": "[WORKFLOW] "+self.data["virtualServer"]["name"]+" creation ("+self.data["virtualServer"]["type"]+", SNAT:"+self.data["virtualServer"]["snat"]+")",
                            "asset_id": self.assetId,
                            "config_object_type": k,
                            "config_object": "/"+self.partitionName+"/"+v["name"],
                            "status": "created"
                            })

                if any(key in k for key in ("node", "poolMember", "profiles")):
                    for n in v:
                        History.add({
                            "username": self.username,
                            "action": "[WORKFLOW] "+self.data["virtualServer"]["name"]+" creation ("+self.data["virtualServer"]["type"]+", SNAT:"+self.data["virtualServer"]["snat"]+")",
                            "asset_id": self.assetId,
                            "config_object_type": k,
                            "config_object": "/"+self.partitionName+"/"+n["name"],
                            "status": "created"
                        })
            except Exception:
                pass
