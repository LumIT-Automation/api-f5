import threading

from f5.models.F5.ltm.Node import Node
from f5.models.F5.ltm.Monitor import Monitor
from f5.models.F5.ltm.Irule import Irule
from f5.models.F5.ltm.Pool import Pool
from f5.models.F5.ltm.SnatPool import SnatPool
from f5.models.F5.ltm.Profile import Profile
from f5.models.F5.sys.Certificate import Certificate
from f5.models.F5.sys.Key import Key
from f5.models.F5.ltm.VirtualServer import VirtualServer
from f5.models.History.History import History

from f5.helpers.Log import Log


class VirtualServerWorkflow:
    def __init__(self, assetId: int, partitionName: str, virtualServerName: str, user: dict, replicaUuid: str, subPath: str = ""):
        try:
            self.profiles = list()
            self.certificates = list()
            self.keys = list()
            self.irules = list()
            self.policies = list()
            self.monitor = {
                "name": "",
                "type": ""
            }
            self.poolName = ""
            self.poolSubPath = ""
            self.snatPool = ""
            self.nodes = list()

            self.__deletedObjects = {
                "node": [],
                "monitor": {},
                "pool": {},
                "poolMember": [],
                "profile": [],
                "certificate": [],
                "key": [],
                "irule": [],
                "snatPool": {},
                "virtualServer": {}
            }

            self.assetId = assetId
            self.partitionName = partitionName
            self.virtualServerName = virtualServerName
            self.subPath = subPath
            self.username = user["username"]
            self.replicaUuid = replicaUuid  # for relating primary/dr operations, when appliable.

            self.__info()
        except Exception as e:
            self.__logFailed()
            raise e



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def delete(self) -> None:
        self.__deleteVirtualServer()
        self.__deleteIrules()
        self.__deleteSnatPool()
        self.__deleteProfiles()
        self.__deleteCertificates()
        self.__deleteKeys()
        self.__deletePool()
        self.__deleteMonitor()
        self.__deleteNodes()

        self.__logDeletedObjects()

        del self



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def relatedF5Objects() -> list:
        return ["node", "monitor", "pool", "poolMember", "snatPool", "irule", "profile", "certificate", "key", "virtualServer"]



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __info(self) -> None:
        try:
            vs = VirtualServer(self.assetId, self.partitionName, self.virtualServerName, self.subPath, loadProfiles=True)

            # General info.
            info = vs.repr()

            infoPoolList = list(filter(bool, info["pool"].split("/"))) # remove the leading element "".
            self.poolName = infoPoolList[-1]
            if len(infoPoolList) > 2:
                self.poolSubPath = '~'.join(infoPoolList[1:-1])

            if "sourceAddressTranslation" in info \
                    and "pool" in info["sourceAddressTranslation"]:
                self.snatPool = info["sourceAddressTranslation"]["pool"]

            for ir in info["rules"]:
                self.irules.append({"name": ir})


            # Related profiles, certificates and keys.
            profiles = info.get("profiles", [])
            for profile in profiles:
                try:
                    details = VirtualServerWorkflow.__getProfileDetails(self.assetId, self.partitionName, profile["name"], profile.get("subPath", ""))
                    self.profiles.append({
                        "name": profile["name"],
                        "subPath": profile.get("subPath", ""),
                        "type": details["type"]
                    })

                    if "cert" in details:
                        self.certificates.append({
                            "name": details["cert"].split("/")[2]
                        })

                    if "key" in details:
                        self.keys.append({
                            "name": details["key"].split("/")[2]
                        })
                except Exception:
                    pass

            # Related policies.
            #policies = vs.policies()["items"]
            #for policy in policies:
            #    self.policies.append(policy["name"])

            if self.poolName:
                # Pool info -> monitor.
                poolInfo = Pool(self.assetId, self.partitionName, self.poolName, self.poolSubPath).info()

                if "monitor" in poolInfo:
                    try:
                        self.monitor["name"] = poolInfo["monitor"].split("/")[2]
                        self.monitor["type"] = VirtualServerWorkflow.__getMonitorDetails(self.assetId, self.partitionName, self.monitor["name"])["type"]
                    except Exception:
                        pass

                # Pool members of self.poolName -> nodes.
                poolMembers = Pool(self.assetId, self.partitionName, self.poolName, self.poolSubPath).getMembersData()
                for pm in poolMembers:
                    self.nodes.append({
                        "name": Node.getNameFromAddress(
                            self.assetId,
                            self.partitionName,
                            pm["address"],
                            silent=True
                        ),
                        "address": pm["address"]
                    })
        except Exception as e:
            raise e


    def __deleteVirtualServer(self) -> None:
        try:
            Log.actionLog("Virtual server deletion workflow: attempting to delete virtual server: "+str(self.virtualServerName))

            vs = VirtualServer(self.assetId, self.partitionName, self.virtualServerName, self.subPath)
            vs.delete()

            self.__deletedObjects["virtualServer"] = {
                "asset": self.assetId,
                "partition": self.partitionName,
                "name": self.virtualServerName
            }
        except Exception as e:
            if e.__class__.__name__ == "CustomException":
                if "F5" in e.payload and e.status == 400 and "in use" in e.payload["F5"]:
                    Log.log("Virtual server "+str(self.virtualServerName)+" in use; not deleting it. ")
                else:
                    Log.log("[ERROR] Virtual server deletion workflow: cannot delete virtual server "+self.virtualServerName+": "+str(e.payload))
            else:
                Log.log("[ERROR] Virtual server deletion workflow: cannot delete virtual server "+self.virtualServerName+": "+e.__str__())

        Log.actionLog("Deleted objects: "+str(self.__deletedObjects))



    def __deleteIrules(self) -> None:
        Log.actionLog("Virtual server deletion workflow: attempting to delete irules: "+str(self.irules))

        for el in self.irules:
            iruleName = el["name"].split("/")[2]
            irulePath = el.get("subPath", "") + "/" + iruleName if el.get("subPath", "") else iruleName

            try:
                Irule(self.assetId, self.partitionName, iruleName, el.get("subPath", "")).delete()

                self.__deletedObjects["irule"].append({
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": irulePath
                })
            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 400 and "in use" in e.payload["F5"]:
                        Log.log("Irule "+str(iruleName)+" in use; not deleting it. ")
                    else:
                        Log.log("[ERROR] Virtual server deletion workflow: cannot delete irule "+iruleName+": "+str(e.payload))
                else:
                    Log.log("[ERROR] Virtual server deletion workflow: cannot delete irule "+iruleName+": "+e.__str__())

        Log.actionLog("Deleted objects: "+str(self.__deletedObjects))



    def __deleteProfiles(self) -> None:
        Log.actionLog("Virtual server deletion workflow: attempting to delete profiles: "+str(self.profiles))

        for p in self.profiles:
            profilePath = p.get("subPath", "") + "/" + p["name"] if p.get("subPath", "") else p["name"]

            try:
                Profile(self.assetId, self.partitionName,  p["type"], p["name"], p.get("subPath", "")).delete()

                self.__deletedObjects["profile"].append({
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": profilePath,
                    "type": p["type"]
                })
            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 400 and "in use" in e.payload["F5"]:
                        Log.log("Profile "+str(p["name"])+" in use; not deleting it. ")
                    else:
                        Log.log("[ERROR] Virtual server deletion workflow: cannot delete profile "+p["name"]+": "+str(e.payload))
                else:
                    Log.log("[ERROR] Virtual server deletion workflow: cannot delete profile "+p["name"]+": "+e.__str__())

        Log.actionLog("Deleted objects: "+str(self.__deletedObjects))



    def __deleteCertificates(self) -> None:
        Log.actionLog("Virtual server deletion workflow: attempting to delete certificates: "+str(self.certificates))

        for c in self.certificates:
            certificateName = c["name"]

            try:
                certificate = Certificate(self.assetId, self.partitionName, certificateName)
                certificate.delete()

                self.__deletedObjects["certificate"].append({
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": certificateName
                })
            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 400 and "in use" in e.payload["F5"]:
                        Log.log("Certificate "+str(certificateName)+" in use; not deleting it. ")
                    else:
                        Log.log("[ERROR] Virtual server deletion workflow: cannot delete certificate "+certificateName+": "+str(e.payload))
                else:
                    Log.log("[ERROR] Virtual server deletion workflow: cannot delete certificate "+certificateName+": "+e.__str__())

        Log.actionLog("Deleted objects: "+str(self.__deletedObjects))



    def __deleteKeys(self) -> None:
        Log.actionLog("Virtual server deletion workflow: attempting to delete keys: "+str(self.keys))

        for k in self.keys:
            keyName = k["name"]

            try:
                key = Key(self.assetId, self.partitionName, keyName)
                key.delete()

                self.__deletedObjects["key"].append({
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": keyName
                })
            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 400 and "in use" in e.payload["F5"]:
                        Log.log("Key "+str(keyName)+" in use; not deleting it. ")
                    else:
                        Log.log("[ERROR] Virtual server deletion workflow: cannot delete key "+keyName+": "+str(e.payload))
                else:
                    Log.log("[ERROR] Virtual server deletion workflow: cannot delete key "+keyName+": "+e.__str__())

        Log.actionLog("Deleted objects: "+str(self.__deletedObjects))



    def __deleteMonitor(self) -> None:
        if self.monitor["name"]:
            try:
                Log.actionLog("Virtual server deletion workflow: attempting to delete monitor: "+str(self.monitor["name"]))

                monitor = Monitor(self.assetId, self.partitionName, self.monitor["type"], self.monitor["name"])
                monitor.delete()

                self.__deletedObjects["monitor"] = {
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": self.monitor["name"],
                    "type": self.monitor["type"]
                }
            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 400 and "in use" in e.payload["F5"]:
                        Log.log("Monitor "+str(self.monitor["name"])+" in use; not deleting it. ")
                    else:
                        Log.log("[ERROR] Virtual server deletion workflow: cannot delete monitor "+self.monitor["name"]+": "+str(e.payload))
                else:
                    Log.log("[ERROR] Virtual server deletion workflow: cannot delete monitor "+self.monitor["name"]+": "+e.__str__())

        Log.actionLog("Deleted objects: "+str(self.__deletedObjects))



    def __deletePool(self) -> None:
        if self.poolName:
            try:
                Log.actionLog("Virtual server deletion workflow: attempting to delete pool: "+str(self.poolName))

                pool = Pool(self.assetId, self.partitionName, self.poolName, self.poolSubPath)
                pool.delete()

                self.__deletedObjects["pool"] = {
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": self.poolName
                }
            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 400 and "in use" in e.payload["F5"]:
                        Log.log("Pool "+str(self.poolName)+" in use; not deleting it. ")
                    else:
                        Log.log("[ERROR] Virtual server deletion workflow: cannot delete pool "+self.poolName+": "+str(e.payload))
                else:
                    Log.log("[ERROR] Virtual server deletion workflow: cannot delete pool "+self.poolName+": "+e.__str__())

        Log.actionLog("Deleted objects: "+str(self.__deletedObjects))



    def __deleteSnatPool(self) -> None:
        if self.snatPool:
            try:
                Log.actionLog("Virtual server deletion workflow: attempting to delete snat pool: "+str(self.snatPool))

                snatpool = SnatPool(self.assetId, self.partitionName, self.snatPool.split("/")[2])
                snatpool.delete()

                self.__deletedObjects["snatPool"] = {
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": self.snatPool
                }
            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 400 and "in use" in e.payload["F5"]:
                        Log.log("Snat pool "+str(self.snatPool)+" in use; not deleting it. ")
                    else:
                        Log.log("[ERROR] Virtual server deletion workflow: cannot delete snat pool "+self.snatPool+": "+str(e.payload))
                else:
                    Log.log("[ERROR] Virtual server deletion workflow: cannot delete snat pool "+self.snatPool+": "+e.__str__())

        Log.actionLog("Deleted objects: "+str(self.__deletedObjects))



    def __deleteNodes(self) -> None:
        Log.actionLog("Virtual server deletion workflow: attempting to delete nodes: "+str(self.nodes))

        for n in self.nodes:
            nodeName = n["name"]
            nodeAddress = n["address"]

            try:
                node = Node(self.assetId, self.partitionName, nodeName)
                node.delete()

                self.__deletedObjects["node"].append({
                    "asset": self.assetId,
                    "partition": self.partitionName,
                    "name": nodeName,
                    "address": nodeAddress
                })
            except Exception as e:
                if e.__class__.__name__ == "CustomException":
                    if "F5" in e.payload and e.status == 400 and "is referenced" in e.payload["F5"]:
                        Log.log("Node "+str(nodeName)+" in use; not deleting it. ")
                    else:
                        Log.log("[ERROR] Virtual server deletion workflow: cannot delete node "+nodeName+": "+str(e.payload))
                else:
                    Log.log("[ERROR] Virtual server deletion workflow: cannot delete node "+nodeName+": "+e.__str__())

        Log.actionLog("Deleted objects: "+str(self.__deletedObjects))



    def __logDeletedObjects(self) -> None:
        for k, v in self.__deletedObjects.items():
            try:
                if k in ("virtualServer", "pool", "monitor", "snatPool"):
                    if "name" in v:
                        History.add({
                            "username": self.username,
                            "action": "[WORKFLOW] "+self.virtualServerName+" deletion",
                            "asset_id": self.assetId,
                            "config_object_type": k,
                            "config_object": "/"+self.partitionName+"/"+v["name"],
                            "status": "deleted",
                            "dr_replica_flow": self.replicaUuid
                            })

                if k in ("node", "profile", "irule", "certificate", "key"):
                    for n in v:
                        History.add({
                            "username": self.username,
                            "action": "[WORKFLOW] "+self.virtualServerName+" deletion",
                            "asset_id": self.assetId,
                            "config_object_type": k,
                            "config_object": "/"+self.partitionName+"/"+n["name"],
                            "status": "deleted",
                            "dr_replica_flow": self.replicaUuid
                        })
            except Exception:
                pass



    def __logFailed(self) -> None:
        try:
            History.add({
                "username": self.username,
                "action": "[WORKFLOW] "+self.virtualServerName+" deletion",
                "asset_id": self.assetId,
                "config_object_type": "virtualServer",
                "config_object": "/"+self.partitionName+"/"+self.virtualServerName,
                "status": "deletion-failed",
                "dr_replica_flow": self.replicaUuid
            })
        except Exception:
            pass



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __getProfileDetails(assetId, partitionName, profileName, subPath):
        profileType = []

        try:
            # The only way to get a profile type is to iterate through all the profile types. A not so small pain in the ass.
            # The threading way. This requires a consistent throttle on remote appliance.
            def profileDetail(a, p, t, n, s):
                try:
                    profileType.append(
                        Profile(a, p, t, n, s).repr()
                    ) # probe.
                except Exception:
                    pass

            profileTypes = Profile.types(assetId, partitionName)
            workers = [threading.Thread(target=profileDetail, args=(assetId, partitionName, m, profileName, subPath)) for m in profileTypes]
            for w in workers:
                w.start()
            for w in workers:
                w.join()

            return profileType[0]
        except Exception as e:
            raise e



    @staticmethod
    def __getMonitorDetails(assetId, partitionName, monitorName):
        monitorType = []

        try:
            def monitorDetail(a, p, t, n):
                try:
                    monitorType.append(
                        Monitor(a, p, t, n).info(silent=True)
                    )
                except Exception:
                    pass

            monitorTypes = Monitor.types(assetId, partitionName)
            workers = [threading.Thread(target=monitorDetail, args=(assetId, partitionName, m, monitorName)) for m in monitorTypes]
            for w in workers:
                w.start()
            for w in workers:
                w.join()

            return monitorType[0]
        except Exception as e:
            raise e
