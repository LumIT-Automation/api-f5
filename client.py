#!/usr/bin/python3

import os
import re
import argparse
import json
import datetime
import logging
import sys
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
            i = Client().get("/api/v1/f5/assets/").json()["data"]["items"]
            return {
                "pro": i[0],
                "nopro": i[1]
            }
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

        if title:
            log.debug(title)

        log.debug(o)



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
    def entityTypeInformation(data: dict) -> dict:
        entityTypeWarning = dict()

        for eType, eList in data["differences"].items():
            ns = 0
            nd = 0
            for l in eList:
                try:
                    if l["diffType"] == "only-in-source":
                        ns += 1
                    if l["diffType"] == "only-in-destination":
                        nd += 1
                    if l["diffType"] == "conflict":
                        if l["sourceLastUpdate"] >= l["destinationLastUpdate"]:
                            ns += 1
                        if l["sourceLastUpdate"] <= l["destinationLastUpdate"]:
                            nd += 1
                except KeyError:
                    pass

            if ns == len(eList):
                entityTypeWarning[eType] = f"All {eType} objects are more newly updated (or new) in source"
            elif nd == len(eList):
                entityTypeWarning[eType] = f"All {eType} objects are more newly updated (or new) in destination"
            elif ns == len(eList) and nd == len(eList):
                entityTypeWarning[eType] = f"All {eType} objects have the same modification timestamp"
            else:
                entityTypeWarning[eType] = ""

        return entityTypeWarning



    @staticmethod
    def newerInformation(element: dict) -> tuple:
        s = d = ""

        try:
            if element["diffType"] == "only-in-source":
                s = " [NEW]"
            elif element["diffType"] == "only-in-destination":
                d = " [NEW]"
            else:
                if element["sourceLastUpdate"] > element["destinationLastUpdate"]:
                    s = " [NEW]"
                elif element["sourceLastUpdate"] < element["destinationLastUpdate"]:
                    d = " [NEW]"
                else:
                    s = d = " [NEW]"
        except KeyError:
            pass

        return s, d



    @staticmethod
    def getIgnoredDifferences(diff: dict, merge: dict) -> dict:
        toBeIgnored = diff["differences"].copy()

        # Get toBeIgnored differences: all diff data but merge elements.
        for de, dl in toBeIgnored.items():
            if de in merge:
                for e in merge[de]: # tuple.
                    jj = 0
                    for vv in dl:
                        if vv["diffType"] in ("conflict", "only-in-source"):
                            if vv["id"] == e[0]:
                                del dl[jj]
                        if vv["diffType"] == "only-in-destination":
                            del dl[jj] # do not count these entries as ignored ones.

                        jj += 1

        for _, dl in toBeIgnored.items():
            for jj, vv in enumerate(dl):
                dl[jj] = {
                    "id": vv["id"],
                    "entityName": vv["entityName"]
                }

        return toBeIgnored



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
    def mergePolicies(dstAssetId: int, destinationPolicyId: str, diffReferenceId: str, mergeDiffsIds: list, deleteDiffsOnDestination: dict) -> str:
        try:
            mergePolicyResponse = Client().post(
                path=f"/api/v1/f5/{dstAssetId}/asm/policy/{destinationPolicyId}/merge/",
                data={
                    "data": {
                        "diffReferenceId": diffReferenceId,
                        "mergeDiffsIds": mergeDiffsIds,
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

Input = {
    "assets": dict(),
    "runs": list()
}

try:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cfg_file', help='Config file to read input from', required=False)
    args = parser.parse_args()

    # Read available config file entries.
    configFile = args.cfg_file or "client-input.json"
    if os.path.exists(str(configFile)):
        with open(configFile, "r") as file:
            iv = json.loads(file.read())

            for environment in ("pro", "nopro"):
                assetsEnv = iv.get("assets", {}).get(environment, {})
                Input["assets"][environment] = {
                    "fqdn": assetsEnv.get("fqdn", ""),
                    "user": assetsEnv.get("user", ""),
                    "password": assetsEnv.get("password", "") or getpass("Insert password for the Pro F5 asset:\n"),
                }

            for run in iv.get("runs", []):
                policiesSource = run.get("policies", {}).get("source", {})
                policiesDestination = run.get("policies", {}).get("destination", {})
                Input["runs"].append({
                    "uuid": run.get("uuid", ""),
                    "policies": {
                        "source": {
                            "asset": policiesSource.get("asset"),
                            "name": policiesSource.get("name"),
                        },
                        "destination": {
                            "asset": policiesDestination.get("asset"),
                            "name": policiesDestination.get("name"),
                        }
                    },
                    "auto-skip": run.get("auto-skip", []),
                    "auto-merge": run.get("auto-merge", []),

                })

        # Check input.
        for k, v in Input["assets"].items():
            for jk, jv in v.items():
                if not jv:
                    Util.out(f"Value not provided: {k}/{jk}", "red", "lightgrey")
                    raise Exception

        uuids = list()
        for v in Input["runs"]:
            if v["uuid"] not in uuids:
                uuids.append(v["uuid"])
            else:
                Util.out("Duplicated uuid: " + v["uuid"], "red", "lightgrey")
                raise Exception

            for _, jv in v["policies"].items():
                for jjk, jjv in jv.items():
                    if not jjv or (jjk == "asset" and jjv not in ("pro", "nopro")):
                        Util.out(f"Value not provided in runs list: {jjk}", "red", "lightgrey")
                        raise Exception
    else:
        Util.out(f"Config file not provided", "red", "lightgrey")
        raise Exception
except Exception as ex:
    Util.out(ex.__str__(), "red", "lightgrey")
    sys.exit()



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
    Asset.loadAsset(ip=Input["assets"]["pro"]["fqdn"], user=Input["assets"]["pro"]["user"], passwd=Input["assets"]["pro"]["password"], environment="pro")
    Asset.loadAsset(ip=Input["assets"]["nopro"]["fqdn"], user=Input["assets"]["nopro"]["user"], passwd=Input["assets"]["nopro"]["password"], environment="nopro")

    loadedAssets = Asset.listAssets()
    if loadedAssets["pro"] and loadedAssets["nopro"]:
        response = ""
        Util.out("Configurations found: ")

        # Ask the user for which run to process amongst found runs.
        for ir, iv in enumerate(Input["runs"]):
            Util.out(str(ir+1) + " - " + str(iv["uuid"]))

        while not response:
                response = input("\nPlease select run(s) to process [type in the corresponding line numbers, e.g.: 1,2,5 or a for all]:\n")

        if re.fullmatch(re.compile(r"^[\d,]+$"), response) or response == "a":
            if response == "a":
                userRuns = Input["runs"]
            else:
                userRuns = list()
                for ur in response.split(","):
                    if ur and 1 <= int(ur) <= len(Input["runs"]):
                        userRuns.append(Input["runs"][int(ur)-1])

            # Process all selected runs.
            for run in userRuns:
                Util.out("\nRUNNING " + run["uuid"], "yellow")

                # Define current assets (chosen from loaded ones), policies and auto-skip/merge for each run.
                srcPolicyName = run["policies"]["source"]["name"]
                dstPolicyName = run["policies"]["destination"]["name"]

                srcAsset = loadedAssets[
                    run["policies"]["source"]["asset"] # pro/nopro.
                ]
                dstAsset = loadedAssets[
                    run["policies"]["destination"]["asset"]
                ]

                autoSkipET = run["auto-skip"]
                autoMergeET = run["auto-merge"]

                # Get the id of the policies given by name.
                srcPolicyId = ASMPolicyManager.getPolicyId(srcAsset["id"], srcPolicyName)
                dstPolicyId = ASMPolicyManager.getPolicyId(dstAsset["id"], dstPolicyName)

                if srcPolicyId and dstPolicyId:
                    Util.out("Processing differences for SOURCE policy " + srcAsset["fqdn"] + "//" + srcPolicyName + " vs DESTINATION policy " + dstAsset["fqdn"] + "//" + dstPolicyName + " on " + dstAsset["fqdn"] + ".")
                    Util.out("This could take a very long while. Logs on \"client.log\" file within the installation folder. Please wait...")

                    # Fetch policies' differences.
                    diffData = ASMPolicyManager.diffPolicies(srcAssetId=srcAsset["id"], sPolicyId=srcPolicyId, dstAssetId=dstAsset["id"], dPolicyId=dstPolicyId)["data"]

                    importedPolicy = diffData["importedPolicy"]
                    Util.out("\nImported policy on destination F5 asset (temp policy):")
                    Util.out("- id: " + importedPolicy["id"])
                    Util.out("- name: " + importedPolicy["name"])
                    Util.out("- destination F5 message:\n" + importedPolicy["import-message"])

                    # Give the diff entity type a modification label.
                    entityTypeInformation = Util.entityTypeInformation(diffData)

                    Util.out("\nDIFFERENCES follow")
                    for diffET, diffLs in diffData["differences"].items():
                        if diffET not in autoSkipET:
                            for el in diffLs:
                                # For each difference print on-screen output and ask the user.
                                if el["diffType"]:
                                    Util.out("\n\n[ENTITY TYPE: " + diffET + "] \"" + el["entityName"] + "\":", "green")
                                    if entityTypeInformation[diffET]:
                                        Util.out(entityTypeInformation[diffET], "yellow")
                                    Util.out("  - difference type: " + el["diffType"] + ";")

                                    sourceWarning, destinationWarning = Util.newerInformation(el)
                                    if "sourceLastUpdate" in el and el["sourceLastUpdate"]:
                                        Util.out("  - source last update " + Util.toDate(el["sourceLastUpdate"]) + sourceWarning + ";")
                                    if "destinationLastUpdate" in el and el["destinationLastUpdate"]:
                                        Util.out("  - destination last update " + Util.toDate(el["destinationLastUpdate"]) + destinationWarning + ";")

                                    # Handle user input.
                                    if diffET in autoMergeET \
                                            and (el["diffType"] == "only-in-source" or el["diffType"] == "only-in-destination" or (el["diffType"] == "conflict" and "NEW" in sourceWarning)):
                                        response = "y" # precompile user response in case of auto-merging.
                                    else:
                                        response = ""

                                    while response not in ("y", "n", "s", "a"):
                                        if not response:
                                            if el["diffType"] in ("conflict", "only-in-source"):
                                                response = input("  -> Merge to destination policy [y/n; d for details; s for skipping the current entity type; a for merging all differences for this entity type]?\n")
                                            else:
                                                response = input("  -> Delete object into destination policy [y/n; d for details; s for skipping the current entity type; a for merging all differences for this entity type]?\n")
                                        elif response == "d":
                                            Util.log(el)
                                            response = ""
                                        else:
                                            Util.out("Type y for yes, n for no, d for details, s for skipping the current entity type, a for merging all differences for this entity type")
                                            response = ""

                                    if response == "y":
                                        # Collect ids to merge subdivided by entity type.
                                        if el["diffType"] in ("conflict", "only-in-source"):
                                            if diffET not in mergeElements:
                                                mergeElements[diffET] = []
                                            mergeElements[diffET].append((el["id"], el["entityName"]))
                                            Util.out("  -> Element will be merged at the end of the collection process, nothing done so far")

                                        # Collect ids for objects to delete on destination subdivided by entity type.
                                        if el["diffType"] == "only-in-destination":
                                            if diffET not in deleteElements:
                                                deleteElements[diffET] = []
                                            deleteElements[diffET].append({"id": el["id"], "entityName": el["entityName"]})
                                            Util.out("  -> Element will be deleted at the end of the collection process, nothing done so far")

                                    if response == "n":
                                        Util.out("  -> Element won't be merged")

                                    if response == "s":
                                        break

                                    if response == "a":
                                        # Collect all ids for this entity type.
                                        for elm in diffData["differences"][diffET]:
                                            if elm["diffType"] in ("conflict", "only-in-source"):
                                                if diffET not in mergeElements:
                                                    mergeElements[diffET] = []

                                                mergeElements[diffET].append((elm["id"], elm["entityName"]))
                                            if elm["diffType"] == "only-in-destination":
                                                if diffET not in deleteElements:
                                                    deleteElements[diffET] = []

                                                deleteElements[diffET].append({"id": elm["id"], "entityName": elm["entityName"]})
                                        break

                    if mergeElements or deleteElements:
                        response = ""
                        Util.log(autoMergeET, "\n\nAutomatically merged entity types: ")
                        Util.log(autoSkipET, "\n\nAutomatically skipped entity types: ")

                        Util.log(mergeElements, "\n\nAttempting to merge the elements (including auto-merged): ")
                        Util.log(deleteElements, "\n\nAttempting to delete the elements from the destination policy: ")

                        Util.log(Util.getIgnoredDifferences(diffData, mergeElements), "\n\nIgnored differences (including auto-skipped): ")

                        # Handle user input.
                        while response not in ("Y", "N"):
                            if not response:
                                response = input("\n\n  -> Confirm merging/deleting the selected differences into the destination policy [Y/N]?\n")
                            else:
                                Util.out("Type Y for yes, N for no")
                                response = ""

                        if response == "Y":
                            # Merge policies.
                            Util.out("\n\nMerging...")
                            Util.out(
                                ASMPolicyManager.mergePolicies(
                                    dstAssetId=dstAsset["id"],
                                    destinationPolicyId=dstPolicyId,
                                    diffReferenceId=diffData["diffReferenceId"],
                                    mergeDiffsIds=[j[0] for j in sum([k for m, k in mergeElements.items()], [])], # plain list of ids.
                                    deleteDiffsOnDestination=deleteElements
                                )
                            )

                            # Policy apply.
                            Util.out("Applying...")
                            Util.out(
                                ASMPolicyManager.applyPolicy(assetId=dstAsset["id"], policyId=dstPolicyId)
                            )

                            Util.out("Done", "green")
                        else:
                            Util.out("Skipping, nothing done", "red", "lightgrey")
                    else:
                        Util.out("No difference to merge, nothing done", "red", "lightgrey")
                else:
                    Util.out("No policy found with given name, skipping", "red", "lightgrey")
        else:
            Util.out("Wrong input, aborting", "red", "lightgrey")
    else:
        Util.out("No asset loaded, aborting", "red", "lightgrey")
except Exception as ex:
    Util.out(ex.__str__(), "red", "lightgrey")
finally:
    Asset.purgeAssets()
