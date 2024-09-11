import re

from django.conf import settings
from django.core.cache import cache

from f5.helpers.Log import Log


class Lock:
    def __init__(self, objectClass: any, o: dict, objectName: str = "", workflowId: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId = ""
        self.partitionName = ""
        self.request = ""
        self.objectClass = objectClass
        self.objectName = objectName

        if workflowId:
            self.workflowId = "_" + workflowId
        else:
            self.workflowId = ""

        if "assetId" in o:
            self.assetId = str(o["assetId"])

        if "partitionName" in o:
            self.partitionName = str(o["partitionName"])

        if "request" in o:
            self.request = str(o["request"])

        # String or list of strings allowed, treat as list.
        if isinstance(self.objectClass, str):
            self.objectClass = [
                self.objectClass
            ]

        if self.objectName == "":
            self.objectName = "any"



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def isUnlocked(self) -> bool:
        # @todo: isUnlocked() / lock() should be atomic.

        #     C    R    U    D
        # C   *    x    *    *
        #
        # R   x    v    x    x
        #
        # U   *    x    *    *
        #
        # D   *    x    *    *

        # *: yes, on different objects.
        # R: read for both singular (info) and plural (list); @todo: improve.
        # Workflows: "*" becomes "x": so always a big lock.

        table = {
            "POST": {
                "POST": "*",
                "GET": "x",
                "PATCH": "*",
                "DELETE": "*",
            },
            "GET": {
                "POST": "x",
                "GET": "v",
                "PATCH": "x",
                "DELETE": "x",
            },
            "PATCH": {
                "POST": "*",
                "GET": "x",
                "PATCH": "*",
                "DELETE": "*",
            },
            "DELETE": {
                "POST": "*",
                "GET": "x",
                "PATCH": "*",
                "DELETE": "*",
            },
        }

        try:
            # Request HTTP method.
            httpMethod = self.__httpMethod()
            if httpMethod:
                # Check if the API endpoint/s related to objectClass are locked for the asset and partition (if set), on objectName,
                # in regards of the HTTP method "compatibility" (see table).
                for oc in self.objectClass:
                    if oc:
                        if str(httpMethod) in table:
                            for method, compatibility in table[httpMethod].items():
                                entry = oc+":"+str(method)+":"+self.assetId+":"+self.partitionName+"*" # add the glob to possibly match the workflowId suffix.

                                # <httpMethod>: {
                                #    "POST": "x",
                                #    "GET": "v",
                                #    "PATCH": "*",
                                #    "DELETE": "*",
                                # }

                                if compatibility == "x":
                                    # Always block if entry present (regardless of its value).
                                    c = cache.get(entry)
                                    # If entry present.
                                    if isinstance(c, dict):
                                        if "lock" in c:
                                            if isinstance(c["lock"], list):
                                                if c["lock"]:
                                                    Log.log("Locked on API.")
                                                    Log.log("Available locks: "+str(c))

                                                    return False

                                if compatibility == "*":
                                    # Block if entry present and objectName in the lock list.
                                    c = cache.get(entry)
                                    # If entry present.
                                    if isinstance(c, dict):
                                        if "lock" in c:
                                            if isinstance(c["lock"], list):
                                                if self.objectName in c["lock"]:
                                                    Log.log("Locked on object "+self.objectName)
                                                    Log.log("Available locks: "+str(c))

                                                    return False
        except Exception:
            pass

        return True



    def lock(self) -> None:
        lockedObjects = [self.objectName]

        # Mark the API endpoint/s related to objectClass as locked for the HTTP method,
        # asset and partition (if set), on objectName.
        # For example: pool:POST:1: = { "lock": ... }
        # For example: pool:POST:1:Common = { "lock": ... }

        # Possible values:
        #   Not set
        #   {'lock': ['any']}
        #   {'lock': ['objectName1', 'objectName2', ...]}
        #   {'lock': ['any', 'objectName3', ...]}

        try:
            httpMethod = self.__httpMethod() # request HTTP method.
            if httpMethod:
                for oc in self.objectClass:
                    if oc:
                        # @todo: a Redis cache transaction lock is needed here.
                        entry = oc+":"+str(httpMethod)+":"+self.assetId+":"+self.partitionName+self.workflowId
                        c = cache.get(entry)

                        # If some locked objectName already set, add the current one.
                        if isinstance(c, dict):
                            if "lock" in c:
                                if self.objectName not in c["lock"]:
                                    c["lock"].append(self.objectName)

                                #lockedObjects = list(dict.fromkeys(c["lock"])) # deduplicate.
                                lockedObjects = c["lock"]

                        cache.set(entry, { "lock": lockedObjects }, timeout=settings.LOCK_MAX_VALIDITY)
                        Log.log("Lock set for "+entry+", which now values "+str(lockedObjects))
        except Exception:
            pass



    def release(self) -> None:
        # Release the lock for objectName for HTTP method/asset/partition.

        try:
            httpMethod = self.__httpMethod() # request HTTP method.
            if httpMethod:
                for oc in self.objectClass:
                    if oc:
                        entry = oc+":"+str(httpMethod)+":"+self.assetId+":"+self.partitionName+self.workflowId
                        c = cache.get(entry)

                        if "lock" in c:
                            if isinstance(c["lock"], list):
                                c["lock"].remove(self.objectName)

                                if c["lock"]:
                                    # Overwrite if c["lock"] not empty.
                                    cache.set(entry, c, timeout=settings.LOCK_MAX_VALIDITY)
                                else:
                                    # Delete the entry completely.
                                    cache.delete(entry)

                                Log.log("Lock released for "+entry+"; now it values: "+str(cache.get(entry)))
        except Exception:
            pass



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def listWorkflowLocks(workflowId:str) -> list:
        try:
            if workflowId:
                globEntries = "*_" + workflowId
                return cache.keys(globEntries)
            else:
                return []
        except Exception as e:
            raise e



    @staticmethod
    def releaseWorkflow(workflowId: str) -> None:
        try:
            entriesList = Lock.listWorkflowLocks(workflowId)
            globEntries = "*_" + workflowId
            cache.delete_pattern(globEntries)
            Log.log("Lock entries released: " + str(entriesList) + " - workflow: " + workflowId + ".")
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __httpMethod(self):
        httpMethod = ""

        if self.request:
            try:
                matches = re.search(r".*:\ (.*)\ '\/", self.request)
                if matches:
                    httpMethod = str(matches.group(1)).strip()
            except Exception:
                pass

        return httpMethod



class Locker():
    def __init__(self, objectClass: str, o: dict, item: str = "", workflowId: str = "", parentObjectClass: str = "", parentItem: str = "", *args, **kwargs):
        self.lockItem = Lock(objectClass, o, item, workflowId)
        self.o = o
        if parentObjectClass:
            self.lockParent = Lock(parentObjectClass, o, parentItem, workflowId)
        else:
            self.lockParent = None

    def isUnlocked(self) -> bool:
        try:
            if self.lockParent:
                if not self.lockParent.isUnlocked():
                    return False

            if self.lockItem.isUnlocked():
                return True

            return False
        except Exception as e:
            raise e


    def lock(self):
        try:
            if self.lockParent:
                self.lockParent.lock()
            self.lockItem.lock()
        except Exception as e:
            raise e

    def release(self):
        try:
            if self.lockParent:
                self.lockParent.release()
            self.lockItem.release()
        except Exception as e:
            raise e

