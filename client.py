#!/usr/bin/python3

import os
import argparse
import json
import datetime

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

import django
from django.conf import settings
from django.test import Client

from f5.helpers.Log import Log



########################################################################################################################
# Parser init
########################################################################################################################

parser = argparse.ArgumentParser()

parser.add_argument('-a', '--src_asset', help='Source F5 asset where the source policy is defined (IP/FQDN)', required=True)
parser.add_argument('-A', '--dst_asset', help='Destination F5 asset where the destination policy is defined (IP/FQDN)', required=True)
parser.add_argument('-l', '--src_policy', help='Source policy name', required=True)
parser.add_argument('-L', '--dst_policy', help='Destination policy name', required=True)
parser.add_argument('-u', '--src_user', help='Source F5 asset username', required=True)
parser.add_argument('-U', '--dst_user', help='Destination F5 asset username', required=True)
parser.add_argument('-p', '--src_passwd', help='Source F5 asset password', required=False)
parser.add_argument('-P', '--dst_passwd', help='Destination F5 asset password', required=False)
#parser.add_argument('-i', '--ignore_entity_types', help='List of entity types to ignore', required=False, action='append')

args = parser.parse_args()

Input = {
    "src": {
        "asset": args.src_asset,
        "user": args.src_user,
        "password": args.src_passwd or input("Insert password for the source F5 asset:\n"),
        "policy": args.src_policy,
    },
    "dst": {
        "asset": args.dst_asset,
        "user": args.dst_user,
        "password": args.dst_passwd or input("Insert password for the destination F5 asset:\n"),
        "policy": args.dst_policy,
    }
}

# ignoreEntityTypes = list()
# if args.ignore_entity_types:
#     ignoreEntityTypes = args.ignore_entity_types



########################################################################################################################
# Django init (Client)
########################################################################################################################

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
settings.DISABLE_AUTHENTICATION = True

settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'f5.db',
    }
}
settings.CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}
settings.REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '600/minute',
        'user': '600/minute'
    }
}
settings.LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'client.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}



########################################################################################################################
# Client
########################################################################################################################

class Asset:
    @staticmethod
    def loadAsset(ip: str, user: str, passwd: str, environment: str) -> None:
        try:
            Client().post(
                path="/api/v1/f5/assets/",
                data={
                    "data": {
                        "address": ip,
                        "fqdn": ip,
                        "baseurl": f"https://{ip}/mgmt/",
                        "tlsverify": 0,
                        "datacenter": "",
                        "environment": environment,
                        "position": "",
                        "username": user,
                        "password": passwd
                    }
                },
                content_type="application/json"
            )
        except Exception as e:
            print(e.args)



    @staticmethod
    def listAssets():
        try:
            return Client().get("/api/v1/f5/assets/").json()
        except Exception as e:
            print(e.args)



    @staticmethod
    def deleteAsset(assetId):
        try:
            return Client().delete(f"/api/v1/f5/asset/{assetId}/")
        except Exception as e:
            print(e.args)



    @staticmethod
    def purgeAssets():
        try:
            return Client().delete("/api/v1/f5/assets/")
        except Exception as e:
            print(e.args)



class Util:
    @staticmethod
    def log(data: object, msg: str = "") -> None:
        try:
            Log.log(data, msg)
            print(msg, str(json.dumps(data, indent=4)))
        except Exception:
            print(msg, str(data))



    @staticmethod
    def out(msg: str) -> None:
        try:
            Log.log(msg)
            print(msg)
        except Exception:
            pass



    @staticmethod
    def toDate(epoch: str):
        epoch = int(epoch)
        if epoch > 10000000000:
            epoch = int(epoch/1000000)

        return datetime.datetime.fromtimestamp(epoch).strftime('%c')



class ASMPolicyManager:
    @staticmethod
    def diffPolicies(srcAssetId: int, dstAssetId: int, sPolicyId: str, dPolicyId: str) -> dict:
        try:
            return Client().get(
                "/api/v1/f5/source-asset/" + str(srcAssetId) + "/destination-asset/" + str(
                    dstAssetId) + "/asm/source-policy/" + sPolicyId + "/destination-policy/" + dPolicyId + "/differences/"
            ).json()
        except Exception as e:
            print(e.args)



    @staticmethod
    def mergePolicies(dstAssetId: int, diffReference: str, diffIds: list = None) -> None:
        diffIds = diffIds or []

        try:
            Client().post(
                path=f"/api/v1/f5/{dstAssetId}/asm/policy-diff/{diffReference}/merge/",
                data={
                    "data": {
                        "diff-ids": diffIds,
                    }
                },
                content_type="application/json"
            )
        except Exception as e:
            print(e.args)



    @staticmethod
    def listPolicies(assetId):
        try:
            return Client().get(f"/api/v1/f5/{assetId}/asm/policies/").json()
        except Exception as e:
            print(e.args)



    @staticmethod
    def getPolicyId(assetId: int, name: str) -> str:
        id = ""

        try:
            id = list(filter(lambda j: j.get("name", "") == name, ASMPolicyManager.listPolicies(assetId)["data"]["items"]))[0]["id"]
        except KeyError:
            pass
        except IndexError:
            pass
        except Exception as e:
            print(e.args)

        return id



########################################################################################################################
# Main
########################################################################################################################

try:
    mergeElements = dict()

    disable_warnings(InsecureRequestWarning)
    django.setup()

    # Load user-inserted assets.
    Asset.loadAsset(ip=Input["src"]["asset"], user=Input["src"]["user"], passwd=Input["src"]["password"], environment="src")
    Asset.loadAsset(ip=Input["dst"]["asset"], user=Input["dst"]["user"], passwd=Input["dst"]["password"], environment="dst")

    loadedAssets = Asset.listAssets()["data"]["items"]
    if loadedAssets[0] and loadedAssets[1]:
        # Get the id of the policies given by name.
        srcPolicyId = ASMPolicyManager.getPolicyId(1, Input["src"]["policy"])
        dstPolicyId = ASMPolicyManager.getPolicyId(2, Input["dst"]["policy"])

        if srcPolicyId and dstPolicyId:
            Util.out("Processing differences for SOURCE policy " + loadedAssets[0]["fqdn"] + "//" + Input["src"]["policy"] + " vs DESTINATION policy " + loadedAssets[1]["fqdn"] + "//" + Input["dst"]["policy"] + " on " + loadedAssets[1]["fqdn"] + ".")
            Util.out("This could take a very long while. Logs on \"client.log\" file within the installation folder. Please wait...")

            # Fetch policies' differences.
            diffData = ASMPolicyManager.diffPolicies(srcAssetId=1, sPolicyId=srcPolicyId, dstAssetId=2, dPolicyId=dstPolicyId)["data"]
            for diffEntityType, diffList in diffData["differences"].items():
                for el in diffList:
                    if el["diffType"] in ("conflict", "only-in-source"):
                        Util.out("\n\n[ENTITY TYPE: " + diffEntityType + "] \"" + el["entityName"] + "\":")
                        Util.out("  - difference type: " + el["diffType"] + ";")
                        if int(el["sourceLastUpdateMicros"]):
                            Util.out("  - source last update " + Util.toDate(el["sourceLastUpdateMicros"]) + ";")
                        if int(el["destinationLastUpdateMicros"]):
                            Util.out("  - destination last update " + Util.toDate(el["destinationLastUpdateMicros"]) + ";") # if conflict.

                        # Handle user input.
                        response = ""
                        while response not in ("y", "n"):
                            if not response:
                                response = input("  -> Merge to destination policy [y/n; d for details]?\n")
                            elif response == "d":
                                Util.log(el)
                                response = ""
                            else:
                                Util.out("Type y for yes, n for no, d for details.")
                                response = ""

                        if response == "y":
                            # Collect ids to merge subdivided by entity type.
                            if diffEntityType not in mergeElements:
                                mergeElements[diffEntityType] = []
                            mergeElements[diffEntityType].append(el["id"])
                            Util.out("  -> Element will be merged at the end of the collection process, nothing done so far.")

                        if response == "n":
                            Util.out("  -> Element won't be merged.")

            if mergeElements:
                response = ""
                Util.log(mergeElements, "\n\nAttempting to merge the elements: ")

                # Handle user input.
                while response not in ("y", "n"):
                    if not response:
                        response = input("  -> Confirm merging the differences into the destination policy [y/n]?\n")
                    else:
                        Util.out("Type y for yes, n for no.")
                        response = ""

                if response == "y":
                    # Merge policy differences by entity type.
                    for mek, mev in mergeElements.items():
                        Util.out(f"Processing {mek} {mev}...")
                        ASMPolicyManager.mergePolicies(dstAssetId=2, diffReference=diffData["diffReferenceId"], diffIds=mergeElements[mek])
            else:
                Util.out("No difference to merge, nothing done.")
        else:
            Util.out("No policy found with given name, aborting.")
    else:
        Util.out("No asset loaded, aborting.")
except Exception as ex:
    Util.log(ex.args)
finally:
    Asset.purgeAssets()
