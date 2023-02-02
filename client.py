#!/usr/bin/python3

import os
import argparse
import json
import datetime
import logging
import tempfile
from getpass import getpass
from colorama import just_fix_windows_console
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

import django
from django.conf import settings
from django.test import Client

just_fix_windows_console() # needed on Windows only.



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
        'LOCATION': os.path.join(tempfile.mkdtemp(), "django_cache"),
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
            raise e



    @staticmethod
    def listAssets() -> dict:
        try:
            return Client().get("/api/v1/f5/assets/").json()
        except Exception as e:
            raise e



    @staticmethod
    def purgeAssets() -> None:
        try:
            Client().delete("/api/v1/f5/assets/")
        except Exception as e:
            raise e



class Util:
    Chars = {
        "reset": '\033[0m',
        "bold": '\033[01m',
        "disable": '\033[02m',
        "underline": '\033[04m',
        "reverse": '\033[07m',
        "strikethrough": '\033[09m',
        "invisible": '\033[08m'
    }

    Fg = {
        "black": '\033[30m',
        "red": '\033[31m',
        "green": '\033[32m',
        "orange": '\033[33m',
        "blue": '\033[34m',
        "purple": '\033[35m',
        "cyan": '\033[36m',
        "lightgrey": '\033[37m',
        "darkgrey": '\033[90m',
        "lightred": '\033[91m',
        "lightgreen": '\033[92m',
        "yellow": '\033[93m',
        "lightblue": '\033[94m',
        "pink": '\033[95m',
        "lightcyan": '\033[96m'
    }

    Bg = {
        "black": '\033[40m',
        "red": '\033[41m',
        "green": '\033[42m',
        "orange": '\033[43m',
        "blue": '\033[44m',
        "purple": '\033[45m',
        "cyan": '\033[46m',
        "lightgrey": '\033[47m'
    }



    @staticmethod
    def baseLog(o: any, title: str = "") -> None:
        log = logging.getLogger("django")
        if title:
            if title == "_":
                for j in range(120):
                    title = title + "_"
            log.debug(title)

        log.debug(o)

        if title:
            log.debug(title)



    @staticmethod
    def log(data: object, msg: str = "") -> None:
        try:
            Util.baseLog(data, msg)
            print(msg, str(json.dumps(data, indent=4)))
        except Exception:
            print(msg, str(data))



    @staticmethod
    def out(msg: str, fg: str = "", bg: str = "") -> None:
        out = ""

        try:
            Util.baseLog(msg)

            if fg:
                out += Util.Fg[fg]
            if bg:
                out += Util.Bg[bg]
            if out:
                out += msg + Util.Chars["reset"]
            else:
                out = msg

            print(out)
        except Exception:
            pass



    @staticmethod
    def toDate(epoch: str) -> str:
        date = "UNKNOWN"

        try:
            epoch = int(epoch)
            if epoch:
                date = datetime.datetime.fromtimestamp(epoch).strftime('%c')
            else:
                date = ""
        except Exception:
            pass

        return date



    @staticmethod
    def getIgnoredDifferences(diff: dict, merge: dict) -> dict:
        ignored = diff["differences"].copy()

        # Get ignored differences: all diff data but merge elements.
        for de, dl in ignored.items():
            if de in merge:
                for e in merge[de]: # tuple.
                    jj = 0
                    for j in dl:
                        if j["id"] == e[0]:
                            del dl[jj]
                        jj += 1

        return ignored



class ASMPolicyManager:
    @staticmethod
    def diffPolicies(srcAssetId: int, dstAssetId: int, sPolicyId: str, dPolicyId: str) -> dict:
        try:
            diffPolicyResponse = Client().get(
                "/api/v1/f5/source-asset/" + str(srcAssetId) + "/destination-asset/" + str(
                    dstAssetId) + "/asm/source-policy/" + sPolicyId + "/destination-policy/" + dPolicyId + "/differences/"
            )
            diffPolicyPayload = diffPolicyResponse.json()

            if diffPolicyResponse.status_code != 200:
                raise Exception(diffPolicyPayload)

            return diffPolicyPayload
        except Exception as e:
            raise e



    @staticmethod
    def mergePolicies(dstAssetId: int, destinationPolicyId: str, importedPolicyId: str, ignoreDiffs: dict, deleteDiffsOnDestination: dict) -> str:
        try:
            mergePolicyResponse = Client().post(
                path=f"/api/v1/f5/{dstAssetId}/asm/policy/{destinationPolicyId}/merge/",
                data={
                    "data": {
                        "importedPolicyId": importedPolicyId,
                        "ignoreDiffs": ignoreDiffs,
                        "deleteDiffsOnDestination": deleteDiffsOnDestination
                    }
                },
                content_type="application/json"
            )
            out = mergePolicyResponse.json()

            if mergePolicyResponse.status_code not in (200, 201):
                raise Exception(out)
        except TypeError:
            out = "" # no JSON returned.
        except Exception as e:
            raise e

        return out



    @staticmethod
    def applyPolicy(assetId: int, policyId: str):
        try:
            applyPolicyResponse = Client().post(
                path=f"/api/v1/f5/{assetId}/asm/policy/{policyId}/apply/",
                data={},
                content_type="application/json"
            )
            out = applyPolicyResponse.json()

            if applyPolicyResponse.status_code not in (200, 201):
                raise Exception(out)
        except TypeError:
            out = "" # no JSON returned.
        except Exception as e:
            raise e

        return out



    @staticmethod
    def listPolicies(assetId) -> dict:
        try:
            policiesResponse = Client().get(f"/api/v1/f5/{assetId}/asm/policies/")
            policiesPayload = policiesResponse.json()

            if policiesResponse.status_code != 200:
                raise Exception(policiesPayload)

            return policiesPayload
        except Exception as e:
            raise e



    @staticmethod
    def getPolicyId(assetId: int, name: str) -> str:
        policyId = ""

        try:
            policies = ASMPolicyManager.listPolicies(assetId)
            policyId = list(filter(lambda j: j.get("name", "") == name, policies["data"]["items"]))[0]["id"]
        except KeyError:
            pass
        except IndexError:
            pass
        except Exception as e:
            raise e

        return policyId



########################################################################################################################
# Parser/config file init
########################################################################################################################

Input = dict()
for j in ("src", "dst"):
    Input[j] = {
        "asset": "",
        "policy": "",
        "user": "",
        "password": "",
    }

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cfg_file', help='Config file to read input from (non-available entries can be taken from cli input)', required=False)
parser.add_argument('-a', '--src_asset', help='Source F5 asset where the source policy is defined (IP/FQDN)', required=False)
parser.add_argument('-A', '--dst_asset', help='Destination F5 asset where the destination policy is defined (IP/FQDN)', required=False)
parser.add_argument('-l', '--src_policy', help='Source policy name', required=False)
parser.add_argument('-L', '--dst_policy', help='Destination policy name', required=False)
parser.add_argument('-u', '--src_user', help='Source F5 asset username', required=False)
parser.add_argument('-U', '--dst_user', help='Destination F5 asset username', required=False)
parser.add_argument('-p', '--src_passwd', help='Source F5 asset password', required=False)
parser.add_argument('-P', '--dst_passwd', help='Destination F5 asset password', required=False)
# parser.add_argument('-i', '--ignore_entity_types', help='List of entity types to ignore', required=False, action='append')

args = parser.parse_args()

# Read available config file entries.
configFile = args.cfg_file or "client-input.json"
if os.path.exists(str(configFile)):
    with open(configFile, "r") as file:
        iv = json.loads(file.read())

        Input = {
            "src": {
                "asset": iv.get("source", {}).get("asset", ""),
                "policy": iv.get("source", {}).get("policy", ""),
                "user": iv.get("source", {}).get("user", ""),
                "password": iv.get("source", {}).get("password", ""),
            },
            "dst": {
                "asset": iv.get("destination", {}).get("asset", ""),
                "policy": iv.get("destination", {}).get("policy", ""),
                "user": iv.get("destination", {}).get("user", ""),
                "password": iv.get("destination", {}).get("password", ""),
            }
        }

# Complete or override entries with user input ones.
try:
    Input = {
        "src": {
            "asset": args.src_asset or Input["src"]["asset"],
            "policy": args.src_policy or Input["src"]["policy"],
            "user": args.src_user or Input["src"]["user"],
            "password": args.src_passwd or Input["src"]["password"] or getpass("Insert password for the source F5 asset:\n")
        },
        "dst": {
            "asset": args.dst_asset or Input["dst"]["asset"],
            "policy": args.dst_policy or Input["dst"]["policy"],
            "user": args.dst_user or Input["dst"]["user"],
            "password": args.dst_passwd  or Input["dst"]["password"] or getpass("Insert password for the destination F5 asset:\n")
        }
    }
except Exception:
    pass

# Check input.
for k, v in Input.items():
    for jk, jv in v.items():
        if not jv:
            Util.out(f"Value not provided: {k}/{jk}", "red", "lightgrey")
            raise Exception

# ignoreEntityTypes = list()
# if args.ignore_entity_types:
#     ignoreEntityTypes = args.ignore_entity_types



########################################################################################################################
# Main
########################################################################################################################

try:
    # Not thread-safe nor concurrency-safe.

    mergeElements = dict()
    deleteElements = dict()

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

            importedPolicy = diffData["importedPolicy"]
            Util.out("\nImported policy on destination F5 asset (temp policy):")
            Util.out("- id: " + importedPolicy["id"])
            Util.out("- name: " + importedPolicy["name"])
            Util.out("- destination F5 message:\n" + importedPolicy["import-message"])

            # Give the diff entity type a modification label.
            sourceEntityTypeIsAllNewer = dict()
            destinationEntityTypeIsAllNewer = dict()
            for diffEntityType, diffList in diffData["differences"].items():
                sourceEntityTypeIsAllNewer[diffEntityType] = True
                destinationEntityTypeIsAllNewer[diffEntityType] = True
                for el in diffList:
                    if el.get("sourceLastUpdate", 0) > el.get("destinationLastUpdate", 0):
                        destinationEntityTypeIsAllNewer[diffEntityType] = False
                    if el.get("sourceLastUpdate", 0) < el.get("destinationLastUpdate", 0):
                        sourceEntityTypeIsAllNewer[diffEntityType] = False

            Util.out("\nDIFFERENCES follow")
            for diffEntityType, diffList in diffData["differences"].items():
                for el in diffList:
                    entityTypeWarning = " "
                    if sourceEntityTypeIsAllNewer[diffEntityType]:
                        entityTypeWarning = "are more newly updated (or new) in source"
                    elif destinationEntityTypeIsAllNewer[diffEntityType]:
                        entityTypeWarning = "are more newly updated (or new) in destination"
                    elif sourceEntityTypeIsAllNewer[diffEntityType] and destinationEntityTypeIsAllNewer[diffEntityType]:
                        entityTypeWarning = "have the same modification timestamp"
                    else:
                        entityTypeWarning = ""

                    # For each difference print on-screen output and ask the user.
                    if el["diffType"] in ("conflict", "only-in-source", "only-in-destination"):
                        Util.out("\n\n[ENTITY TYPE: " + diffEntityType + "] \"" + el["entityName"] + "\":", "green")
                        if entityTypeWarning:
                            Util.out(f"[All {diffEntityType} objects {entityTypeWarning}]", "yellow")
                        Util.out("  - difference type: " + el["diffType"] + ";")

                        sourceWarning = destinationWarning = ""
                        try:
                            if el.get("sourceLastUpdate", 0) >= el.get("destinationLastUpdate", 0):
                                sourceWarning = " [NEW]"
                            else:
                                destinationWarning = " [NEW]"
                        except Exception:
                            pass

                        if "sourceLastUpdate" in el and el["sourceLastUpdate"]:
                            Util.out("  - source last update " + Util.toDate(el["sourceLastUpdate"]) + sourceWarning + ";")
                        if "destinationLastUpdate" in el and el["destinationLastUpdate"]:
                            Util.out("  - destination last update " + Util.toDate(el["destinationLastUpdate"]) + destinationWarning + ";")

                        # Handle user input.
                        response = ""
                        while response not in ("y", "n", "s", "a"):
                            if not response:
                                if el["diffType"] in ("conflict", "only-in-source"):
                                    response = input("  -> Merge to destination policy [y/n; d for details; s for skipping the current entity type; a for merging all differences for this entity type]?\n")
                                else:
                                    response = input("  -> Delete object into destination policy [y/n; d for details; s for skipping the current entity type; a for merging all differences for this entity type] [@todo: not implemented]?\n")
                            elif response == "d":
                                Util.log(el)
                                response = ""
                            else:
                                Util.out("Type y for yes, n for no, d for details, s for skipping the current entity type, a for merging all differences for this entity type")
                                response = ""

                        if response == "y":
                            # Collect ids to merge subdivided by entity type.
                            if el["diffType"] in ("conflict", "only-in-source"):
                                if diffEntityType not in mergeElements:
                                    mergeElements[diffEntityType] = []
                                mergeElements[diffEntityType].append((el["id"], el["entityName"]))
                                Util.out("  -> Element will be merged at the end of the collection process, nothing done so far")

                            # Collect ids for objects to delete on destination subdivided by entity type.
                            if el["diffType"] == "only-in-destination":
                                if diffEntityType not in deleteElements:
                                    deleteElements[diffEntityType] = []
                                deleteElements[diffEntityType].append((el["id"], el["entityName"]))
                                Util.out("  -> Element will be deleted at the end of the collection process, nothing done so far")

                        if response == "n":
                            Util.out("  -> Element won't be merged")

                        if response == "s":
                            break

                        if response == "a":
                            # Collect all ids for this entity type.
                            if diffEntityType not in mergeElements:
                                mergeElements[diffEntityType] = []
                            if diffEntityType not in deleteElements:
                                deleteElements[diffEntityType] = []

                            for elm in diffData["differences"][diffEntityType]:
                                if elm["diffType"] in ("conflict", "only-in-source"):
                                    mergeElements[diffEntityType].append((elm["id"], elm["entityName"]))
                                if elm["diffType"] == "only-in-destination":
                                    deleteElements[diffEntityType].append((elm["id"], elm["entityName"]))
                            break

            if mergeElements or deleteElements:
                response = ""
                Util.log(mergeElements, "\n\nAttempting to merge the elements: ")
                Util.log(deleteElements, "\n\nAttempting to delete the elements from the destination policy: ")

                # Handle user input.
                while response not in ("Y", "N"):
                    if not response:
                        response = input("  -> Confirm merging/deleting the selected differences into the destination policy [Y/N]?\n")
                    else:
                        Util.out("Type Y for yes, N for no")
                        response = ""

                if response == "Y":
                    # Merge policies.
                    Util.out("\n\nMerging...")
                    Util.out(
                        ASMPolicyManager.mergePolicies(
                            dstAssetId=2,
                            destinationPolicyId=dstPolicyId,
                            importedPolicyId=importedPolicy["id"],
                            ignoreDiffs=Util.getIgnoredDifferences(diffData, mergeElements),
                            deleteDiffsOnDestination=deleteElements
                        )
                    )

                    # Policy apply.
                    Util.out("Applying...")
                    Util.out(
                        ASMPolicyManager.applyPolicy(assetId=2, policyId=dstPolicyId)
                    )

                    Util.out("All done", "green")
                else:
                    Util.out("Quitting, nothing done", "red", "lightgrey")
            else:
                Util.out("No difference to merge, nothing done", "red", "lightgrey")
        else:
            Util.out("No policy found with given name, aborting", "red", "lightgrey")
    else:
        Util.out("No asset loaded, aborting", "red", "lightgrey")
except Exception as ex:
    Util.out(ex.__str__(), "red", "lightgrey")
finally:
    Asset.purgeAssets()
