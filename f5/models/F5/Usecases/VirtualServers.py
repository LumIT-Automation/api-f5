import re

from collections import OrderedDict

from f5.models.F5.ltm.Node import Node
from f5.models.F5.ltm.Monitor import Monitor
from f5.models.F5.ltm.Pool import Pool
from f5.models.F5.sys.Certificate import Certificate
from f5.models.F5.sys.Key import Key
from f5.models.F5.ltm.SnatPool import SnatPool
from f5.models.F5.ltm.Profile import Profile
from f5.models.F5.ltm.Irule import Irule
from f5.models.F5.ltm.VirtualServer import VirtualServer
from f5.models.History.History import History

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException


class VirtualServersWorkflow:
    def __init__(self, assetId: int, partitionName: str, data: dict, user: dict, replicaUuid: str):
        self.assetId = assetId
        self.partitionName = partitionName
        self.data = data
        self.username = user["username"]
        self.replicaUuid = replicaUuid # for relating primary/dr operations, when appliable.
        self.routeDomain = ""

        if "routeDomainId" in data["virtualServer"] and data["virtualServer"]["routeDomainId"]:
            self.routeDomain = "%"+str(data["virtualServer"]["routeDomainId"]) # for example: %1.

        self.__createdObjects = {
            "node": [],
            "monitor": {},
            "pool": {},
            "poolMember": [],
            "irule": [],
            "profile": [],
            "snatPool": {},
            "key": [],
            "certificate": [],
            "virtualServer": {}
        }

        self.__usedObjects = {
            "node": []
        }



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def add(self) -> None:
        try:
            #vsType = self.data["virtualServer"]["type"]

            self.__createNodes()
            self.__createMonitor()
            self.__createPool()
            self.__createPoolMembers()
            self.__createSnatPool()
            self.__createIrules()
            self.__createProfiles()
            self.__createVirtualServer()

            self.__logCreatedObjects()
        except KeyError:
            self.__cleanCreatedObjects()
            raise CustomException(status=400, payload={"F5": "Wrong input."})
        except Exception as e:
            self.__logFailed()
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def relatedF5Objects() -> list:
        return ["node", "monitor", "pool", "poolMember", "snatPool", "irule", "profile", "certificate", "key", "virtualServer"]



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __createNodes(self) -> None:
        j = 0

        for el in self.data["pool"]["nodes"]:
            nodeName = el["name"]
            nodeSubPath = el.get('nodeSubPath', '')
            nodePath = nodeSubPath + "/" + nodeName if nodeSubPath else nodeName
            nodeAddress = el["address"]

            if nodeName == nodeAddress:
                self.data["pool"]["nodes"][j]["name"] = nodeName = "node_"+nodeName # this fixes an F5 issue (name = address when using a root domain different than the default).

            if not re.match('^.*%[0-9]+$', nodeAddress):
                nodeAddress = nodeAddress + self.routeDomain

            try:
                Log.actionLog("Virtual server workflow: attempting to create node: "+str(nodeAddress))

                Node.add(self.assetId, {
                    "name": nodeName,
                    "subPath": nodeSubPath,
                    "address": nodeAddress,
                    "partition": self.partitionName,
                    "State": "up"
                })

                # Keep track of CREATED nodes.
                self.__createdObjects["node"].append({
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": nodePath,
                    "address": nodeAddress,
                })
            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 409 and "already exists" in e.payload["F5"]:
                        Log.log("Node "+str(nodeName)+"/"+str(nodeAddress)+" already exists with the same address/name; using it. ")

                        # Keep track of USED node.
                        self.__usedObjects["node"].append({
                            "asset": self.assetId,
                            "partition": self.partitionName,
                            "name": nodePath,
                            "address": nodeAddress,
                        })
                    else:
                        self.__cleanCreatedObjects()
                        raise e
                else:
                    self.__cleanCreatedObjects()
                    raise e

            j += 1

        Log.actionLog("Created objects: "+str(self.__createdObjects))
        Log.actionLog("Reused existent objects: "+str(self.__usedObjects))



    def __createMonitor(self) -> None:
        if "monitor" in self.data:
            monitorName = self.data["monitor"]["name"]
            monitorSubPath = self.data["monitor"].get('monitorSubPath', '')
            monitorPath = monitorSubPath + "/" + monitorName if monitorSubPath else monitorName
            monitorType = self.data["monitor"]["type"]

            try:
                Log.actionLog("Virtual server workflow: attempting to create monitor: "+str(monitorName))

                mData = {
                    "name": monitorName,
                    "subPath": monitorSubPath,
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
                    "name": monitorPath,
                    "type": monitorType
                }

            except Exception as e:
                self.__cleanCreatedObjects()
                raise e

            Log.actionLog("Created objects: "+str(self.__createdObjects))



    def __createPool(self) -> None:
        poolName = self.data["pool"]["name"]
        poolSubPath = self.data["pool"].get('poolSubPath', '')
        poolPath = poolSubPath + "/" + poolName if poolSubPath else poolName

        try:
            Log.actionLog("Virtual server workflow: attempting to create pool: "+str(poolName))

            Pool.add(self.assetId, {
                "name": poolName,
                "subPath": poolSubPath,
                "partition": self.partitionName,
                "monitor": "/"+self.partitionName+"/"+self.__createdObjects["monitor"]["name"],
                "loadBalancingMode": self.data["pool"]["loadBalancingMode"]
            })

            # Keep track of CREATED pool.
            self.__createdObjects["pool"] = {
                "asset": self.assetId,
                "partition": self.partitionName,
                "name": poolPath,
            }
        except Exception as e:
            self.__cleanCreatedObjects()
            raise e

        Log.actionLog("Created objects: "+str(self.__createdObjects))



    def __createPoolMembers(self) -> None:
        poolName = self.data["pool"]["name"]
        poolSubPath = self.data["pool"].get('poolSubPath', '')
        poolPath = poolSubPath + "/" + poolName if poolSubPath else poolName

        if "nodes" in self.data["pool"]:
            for el in self.data["pool"]["nodes"]:
                nodeName = el["name"]
                nodeSubPath = el.get('nodeSubPath', '')
                nodePath = nodeSubPath+"/"+nodeName+":"+str(el["port"]) if nodeSubPath else nodeName+":"+str(el["port"])

                try:
                    Log.actionLog("Virtual server workflow: attempting to create pool members: associate "+str(nodeName)+" to "+str(poolName)+" on port "+str(el["port"]))

                    Pool(self.assetId, self.partitionName, poolName, poolSubPath).addMember({
                            "name": "/"+self.partitionName+"/"+nodePath,
                            "State": "up",
                            "session": "user-enabled"
                        }
                    )

                    # Keep track of CREATED pool members.
                    self.__createdObjects["poolMember"].append({
                        "asset": self.assetId,
                        "partition": self.partitionName,
                        "pool": poolPath,
                        "name": nodePath
                    })
                except Exception as e:
                    self.__cleanCreatedObjects()
                    raise e

            Log.actionLog("Created objects: "+str(self.__createdObjects))



    def __createIrules(self) -> None:
        if "irules" in self.data:
            for el in self.data["irules"]:
                iruleName = el["name"]
                iruleSubPath = el.get('iruleSubPath', '')
                irulePath = iruleSubPath + "/" + iruleName if iruleSubPath else iruleName

                iruleCode = ""
                if "code" in el:
                    iruleCode = el["code"]

                try:
                    Log.actionLog("Virtual server workflow: attempting to create irule: "+str(iruleName))

                    Irule.add(self.assetId, {
                        "name": iruleName,
                        "subPath": iruleSubPath,
                        "partition": self.partitionName,
                        "apiAnonymous": iruleCode
                    })

                    # Keep track of CREATED irule.
                    self.__createdObjects["irule"].append({
                        "asset": self.assetId,
                        "partition": self.partitionName,
                        "name": irulePath
                    })
                except Exception as e:
                    self.__cleanCreatedObjects()
                    raise e

            Log.actionLog("Created objects: "+str(self.__createdObjects))



    def __createCertificateOrKey(self, o: str, name: str, text: str) -> None:
        if o in ("certificate", "key"):
            try:
                Log.actionLog("Virtual server workflow: attempting to create "+o+": "+str(name))

                if o == "certificate":
                    Certificate.install(self.assetId, self.partitionName, {
                        "name": name,
                        "content_base64": text
                    })
                else:
                    Key.install(self.assetId, self.partitionName, {
                        "name": name,
                        "content_base64": text
                    })

                # Keep track of CREATED object.
                self.__createdObjects[o].append({
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": name
                })
            except Exception as e:
                self.__cleanCreatedObjects()
                raise e

            Log.actionLog("Created objects: "+str(self.__createdObjects))
        else:
            raise NotImplementedError



    def __createProfiles(self) -> None:
        for el in self.data["profiles"]:
            profileName = el["name"]
            profileType = el["type"]
            profileSubPath = el.get('profileSubPath', '')
            profilePath = profileSubPath + "/" + profileName if profileSubPath else profileName

            data = {
                "name": profileName,
                "subPath": profileSubPath,
                "partition": self.partitionName
            }

            # Additional POST data.
            if "idleTimeout" in el:
                data["idleTimeout"] = el["idleTimeout"]
            if "defaultsFrom" in el:
                data["defaultsFrom"] = el["defaultsFrom"]

            try:
                # Create key and certificate.
                certName = keyName = chainName = self.data["virtualServer"]["name"]

                if "cert" in el and el["cert"]:
                    if "certName" in el \
                            and el["certName"]:
                        certName = el["certName"]

                    self.__createCertificateOrKey("certificate", name=certName, text=el["cert"])
                    data["cert"] = "/"+self.partitionName+"/"+certName # use the created one.

                if "key" in el and el["key"]:
                    if "keyName" in el \
                            and el["keyName"]:
                        keyName = el["keyName"]

                    self.__createCertificateOrKey("key", name=keyName, text=el["key"])
                    data["key"] = "/"+self.partitionName+"/"+keyName

                if "chain" in el and el["chain"]:
                    if "chainName" in el \
                            and el["chainName"]:
                        chainName = el["chainName"]

                    self.__createCertificateOrKey("certificate", name=chainName, text=el["chain"])
                    data["chain"] = "/"+self.partitionName+"/"+chainName

                # Create profile.
                Log.actionLog("Virtual server workflow: attempting to create profile: "+str(profileName))

                Profile.add(self.assetId, profileType, data)

                # Keep track of CREATED profile.
                self.__createdObjects["profile"].append({
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": profilePath,
                    "type": profileType
                })
            except Exception as e:
                self.__cleanCreatedObjects()
                raise e

        Log.actionLog("Created objects: "+str(self.__createdObjects))



    def __createSnatPool(self) -> None:
        if self.data["virtualServer"]["snat"] == "snat":
            if "snatPool" in self.data:
                snatPoolName = self.data["snatPool"]["name"]
                snatPoolSubPath = self.data["snatPool"].get('snatPoolSubPath', '')
                snatPoolPath = snatPoolSubPath + "/" + snatPoolName if snatPoolSubPath else snatPoolName
                snatPoolMembers = list()

                try:
                    Log.actionLog("Virtual server workflow: attempting to create SNAT pool: "+str(snatPoolName))

                    if "members" in self.data["snatPool"]:
                        for m in self.data["snatPool"]["members"]:
                            snatPoolMembers.append("/"+self.partitionName+"/"+m+self.routeDomain)

                    SnatPool.add(self.assetId, {
                        "name": snatPoolName,
                        "subPath": snatPoolSubPath,
                        "partition": self.partitionName,
                        "members": snatPoolMembers
                    })

                    # Keep track of CREATED snatPool.
                    self.__createdObjects["snatPool"] = {
                        "asset": self.assetId,
                        "partition": self.partitionName,
                        "name": snatPoolPath
                    }
                except Exception as e:
                    self.__cleanCreatedObjects()
                    raise e

            Log.actionLog("Created objects: "+str(self.__createdObjects))
        else:
            Log.actionLog("Snat pool creation skipped.")



    def __createVirtualServer(self) -> None:
        profiles = list()
        irules = list()

        virtualServerName = self.data["virtualServer"]["name"]
        virtualServerDestination = self.data["virtualServer"]["destination"]
        virtualServerMask = self.data["virtualServer"]["mask"]
        virtualServerSource = self.data["virtualServer"]["source"]

        try:
            Log.actionLog("Virtual server workflow: attempting to create virtual server: "+str(virtualServerName))

            virtualServerSnat = {
                "type": self.data["virtualServer"]["snat"],
                "pool": self.data.get("snatPool", {}).get("name", "")
            }

            if self.routeDomain:
                i, m = virtualServerSource.split("/")
                virtualServerSource = i + self.routeDomain + "/" + m

                i, p = virtualServerDestination.split(":")
                virtualServerDestination = i + self.routeDomain + ":" + p

            if "profiles" in self.data:
                for el in self.data["profiles"]:
                    context = "all"
                    if "context" in el:
                        context = el["context"]

                    profilePath = el.get('profileSubPath', '')+"/"+el["name"] if el.get('profileSubPath', '') else el["name"]
                    profiles.append({
                        "name": "/"+self.partitionName+"/"+profilePath,
                        "context": context
                    })

            if "irules" in self.data:
                for el in self.data["irules"]:
                    irulePath = el.get('iruleSubPath', '')+"/"+el["name"] if el.get('iruleSubPath', '') else el["name"]
                    irules.append("/"+self.partitionName+"/"+irulePath)

            poolPath = self.data["pool"].get('poolSubPath', '')+"/"+self.data["pool"]["name"] if self.data["pool"].get('poolSubPath', '') else self.data["pool"]["name"]

            VirtualServer.add(self.assetId, {
                "name": virtualServerName,
                "subPath": self.data["virtualServer"].get("subPath", ""),
                "partition": self.partitionName,
                "destination": "/"+self.partitionName+"/"+virtualServerDestination,
                "ipProtocol": "tcp",
                "rules": irules,
                "profiles": profiles,
                "mask": virtualServerMask,
                "pool":  "/"+self.partitionName+"/"+poolPath,
                "source": virtualServerSource,
                "sourceAddressTranslation": virtualServerSnat
            })

            # Keep track of CREATED virtual server.
            self.__createdObjects["virtualServer"] = {
                "asset": self.assetId,
                "partition": self.partitionName,
                "name": virtualServerName
            }
        except Exception as e:
            self.__cleanCreatedObjects()
            raise e

        Log.actionLog("Created objects: "+str(self.__createdObjects))


    
    def __cleanCreatedObjects(self):
        Log.log("Virtual server workflow: cleanup")

        # Reverse elements in order to delete from leaf to branch.
        self.__createdObjects = OrderedDict(
            reversed(list(
                self.__createdObjects.items())
            )
        )

        for k, v in self.__createdObjects.items():
            if k == "virtualServer":
                if "name" in v:
                    virtualServerName = v["name"]
                    subPath = v.get("subPath", "")
                    try:
                        Log.log("Virtual server workflow: cleanup virtualServer "+virtualServerName)

                        vs = VirtualServer(self.assetId, self.partitionName, virtualServerName, subPath)
                        vs.delete()
                    except Exception:
                        # If deletion failed, log.
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+virtualServerName)

            if k == "irule":
                for n in v:
                    iruleName = n["name"]
                    iruleSubPath = n.get("iruleSubPath", "")
                    try:
                        Log.log("Virtual server workflow: cleanup irule "+iruleName)

                        irule = Irule(self.assetId, self.partitionName, iruleName, iruleSubPath)
                        irule.delete()
                    except Exception:
                        # If deletion failed, log.
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+iruleName)

            if k == "profile":
                for n in v:
                    profileName = n["name"]
                    profileSubPath = n.get("profileSubPath", "")
                    profileType = n["type"]
                    try:
                        Log.log("Virtual server workflow: cleanup profile "+profileName)

                        profile = Profile(self.assetId, self.partitionName, profileType, profileName, profileSubPath)
                        profile.delete()
                    except Exception:
                        # If deletion failed, log.
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+profileName)

            if k == "certificate":
                for n in v:
                    certificateName = n["name"]
                    try:
                        Log.log("Virtual server workflow: cleanup certificate "+certificateName)

                        certificate = Certificate(self.assetId, self.partitionName, certificateName)
                        certificate.delete()
                    except Exception:
                        # If deletion failed, log.
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+certificateName)

            if k == "key":
                for n in v:
                    keyName = n["name"]
                    try:
                        Log.log("Virtual server workflow: cleanup certificate "+keyName)

                        key = Key(self.assetId, self.partitionName, keyName)
                        key.delete()
                    except Exception:
                        # If deletion failed, log.
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+keyName)

            if k == "poolMember":
                for n in v:
                    poolMemberName = n["name"]
                    nodeSubPath = n.get("nodeSubPath", "")
                    poolName = n["pool"]
                    poolSubPath = n.get("poolSubPath", "")
                    try:
                        Log.log("Virtual server workflow: cleanup pool member "+poolMemberName)

                        poolMember = Pool(self.assetId, poolName, self.partitionName, poolSubPath).getMember(poolMemberName, nodeSubPath)
                        poolMember.delete()
                    except Exception:
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+poolMemberName)

            if k == "pool":
                if "name" in v:
                    poolName = v["name"]
                    poolSubPath = n.get("poolSubPath", "")
                    try:
                        Log.log("Virtual server workflow: cleanup pool "+poolName)

                        pool = Pool(self.assetId, self.partitionName, poolName, poolSubPath)
                        pool.delete()
                    except Exception:
                        # If deletion failed, log.
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+poolName)

            if k == "snatPool":
                if "name" in v:
                    snatPoolName = v["name"]
                    snatPoolSubPath = n.get("snatPoolSubPath", "")
                    try:
                        Log.log("Virtual server workflow: cleanup snatpool "+snatPoolName)

                        snatpool = SnatPool(self.assetId, self.partitionName, snatPoolName, snatPoolSubPath)
                        snatpool.delete()
                    except Exception:
                        # If deletion failed, log.
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+snatPoolName)

            if k == "monitor":
                if "name" in v:
                    monitorName = v["name"]
                    monitorSubPath = v.get("monitorSubPath", "")
                    monitorType = v["type"]
                    try:
                        Log.log("Virtual server workflow: cleanup monitor "+monitorName)

                        monitor = Monitor(self.assetId, self.partitionName, monitorType, monitorName, monitorSubPath)
                        monitor.delete()
                    except Exception:
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+monitorName)

            if k == "node":
                for n in v:
                    nodeName = n["name"]
                    nodeSubPath = n.get("nodeSubPath", "")
                    try:
                        Log.log("Virtual server workflow: cleanup node "+nodeName)

                        node = Node(self.assetId, self.partitionName, nodeName, nodeSubPath)
                        node.delete()
                    except Exception:
                        Log.actionLog("[ERROR] Virtual server workflow: failed to clean "+nodeName)



    def __logCreatedObjects(self) -> None:
        for k, v in self.__createdObjects.items():
            try:
                if k in ("virtualServer", "pool", "monitor", "snatPool"):
                    if "name" in v:
                        History.add({
                            "username": self.username,
                            "action": "[WORKFLOW] "+self.data["virtualServer"]["name"]+" creation ("+self.data["virtualServer"]["type"]+", SNAT:"+self.data["virtualServer"]["snat"]+")",
                            "asset_id": self.assetId,
                            "config_object_type": k,
                            "config_object": "/"+self.partitionName+"/"+v["name"],
                            "status": "created",
                            "dr_replica_flow": self.replicaUuid
                            })

                if k in ("node", "poolMember", "irule", "profile", "key", "certificate"):
                    for n in v:
                        History.add({
                            "username": self.username,
                            "action": "[WORKFLOW] "+self.data["virtualServer"]["name"]+" creation ("+self.data["virtualServer"]["type"]+", SNAT:"+self.data["virtualServer"]["snat"]+")",
                            "asset_id": self.assetId,
                            "config_object_type": k,
                            "config_object": "/"+self.partitionName+"/"+n["name"],
                            "status": "created",
                            "dr_replica_flow": self.replicaUuid
                        })
            except Exception:
                pass



    def __logFailed(self) -> None:
        try:
            History.add({
                "username": self.username,
                "action": "[WORKFLOW] "+self.data["virtualServer"]["name"]+" creation ("+self.data["virtualServer"]["type"]+", SNAT:"+self.data["virtualServer"]["snat"]+")",
                "asset_id": self.assetId,
                "config_object_type": "virtualServer",
                "config_object": "/"+self.partitionName+"/"+self.data["virtualServer"]["name"],
                "status": "creation-failed",
                "dr_replica_flow": self.replicaUuid
                })
        except Exception:
            pass
