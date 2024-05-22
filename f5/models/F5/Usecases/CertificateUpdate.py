from f5.models.F5.sys.Certificate import Certificate
from f5.models.F5.sys.Key import Key
from f5.models.F5.ltm.Profile import Profile

from f5.models.History.History import History

from f5.helpers.Log import Log
from f5.helpers.Exception import CustomException


class CertificateUpdateWorkflow():
    def __init__(self, assetId: int, partitionName: str, profileName: str, user: dict, replicaUuid: str, *args, **kwargs):

        self.assetId = assetId
        self.partitionName = partitionName
        self.sslProfile = profileName
        self.username = user["username"]
        self.replicaUuid = replicaUuid




    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def updateCert(self, data: dict) -> None:
        try:
            self.__certInstall(data["certificate"])

            dataKey = data.get("key", {})
            if dataKey:
                self.__keyInstall(dataKey)
                Key.install(self.assetId, self.partitionName, data["key"])

            profileData = {
                "cert": "/" + self.partitionName + "/" + data["certificate"]["name"],
                "key": "/" + self.partitionName + "/" + data.get("key", {}).get("name", "")
            }
            self.__updateProfile(profileData, data.get("virtualServerName", ""))

        except Exception as e:
            raise e



    ####################################################################################################################
    # Private methods
    ####################################################################################################################

    def __certInstall(self, data: dict):
        try:
            Certificate.install(self.assetId, self.partitionName, data)
            self.__log(action="[WORKFLOW] Install Certificate", objectType="cert", object=data.get("name", ""), status="installed")

        except Exception as e:
            self.__log(action="[ERROR] Install Certificate Workflow:", objectType="cert", object=data.get("name", ""), status="not installed")
            raise CustomException(status=400, payload={"message": "Certificate install failed."})



    def __keyInstall(self, data: dict):
        try:
            Key.install(self.assetId, self.partitionName, data)
            self.__log(action="[WORKFLOW] Install Private Key", objectType="key", object=data.get("name", ""), status="installed")

        except Exception as e:
            self.__log(action="[ERROR] Install Private Key Workflow:", objectType="key", object=data.get("name", ""), status="not installed")
            raise CustomException(status=400, payload={"message": "Private key install failed."})



    def __updateProfile(self, data: dict, virtualServerName: str = ""):
        action = "Update SSL Profile"
        if virtualServerName:
            action += " of Virtualserver: " + virtualServerName

        try:
            Profile(self.assetId, self.partitionName, "client-ssl", self.sslProfile).modify(data)
            self.__log(action="[WORKFLOW] " + action, objectType="client-ssl profile", object=str(data), status="updated")

        except Exception as e:
            self.__log(action="[ERROR] Workflow " + action, objectType="client-ssl profile", object=str(data), status="not updated")
            raise CustomException(status=400, payload={"message": "Update client-ssl profile failed."})



    def __log(self, action: str, objectType: str, object: str, status: str) -> None:
        try:
            Log.actionLog(action+" Flow: "+self.replicaUuid+" assetId: "+str(self.assetId)+" partition: "+self.partitionName+" object type: "+objectType+" object name: "+object+" status: "+status, self.username)

            History.add({
                "username": self.username,
                "action": action,
                "asset_id": self.assetId,
                "config_object_type": objectType,
                "config_object": object,
                "status": status,
                "dr_replica_flow": self.replicaUuid
                })
        except Exception:
            pass
