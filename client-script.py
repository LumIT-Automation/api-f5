#!/usr/bin/python3

import os
import argparse
import json

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

import django
from django.db import connection
from django.conf import settings
from django.test import Client



########################################################################################################################
# Parser init
########################################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--src_asset', help='Source asset of the policies (ip/hostname)', required=True)
parser.add_argument('-A', '--dst_asset', help='Destination asset of the policies (ip/hostname)', required=True)
parser.add_argument('-u', '--src_user', help='Source asset username (default: admin)', required=False)
parser.add_argument('-U', '--dst_user', help='Destination asset username (default: admin)', required=False)
parser.add_argument('-p', '--src_passwd', help='Source asset password', required=False)
parser.add_argument('-P', '--dst_passwd', help='Destination asset password', required=False)
args = parser.parse_args()

srcIpAsset = args.src_asset
dstIpAsset = args.dst_asset

if args.src_user:
    srcUser = args.src_user
else:
    srcUser = 'admin'
if args.dst_user:
    dstUser = args.dst_user
else:
    dstUser = 'admin'

if args.src_passwd:
    srcPasswd = args.src_passwd
else:
    srcPasswd = input("Insert password for the source asset:\n")
if args.dst_passwd:
    dstPasswd = args.dst_passwd
else:
    dstPasswd = input("Insert password for the destination asset:\n")



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
            'filename': '/tmp/django.log',
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
        # Raw method for sqlite to reset the autoincrement index.
        c = connection.cursor()

        try:
            c.execute("DELETE FROM asset")
            connection.commit()
            c.execute("UPDATE sqlite_sequence SET seq=0 WHERE name='asset'")
        except Exception as e:
            print(e.args)
        finally:
            c.close()



class Util:
    @staticmethod
    def log(data: object, msg: str = "") -> None:
        # @todo: Log.log().

        try:
            print(msg, str(json.dumps(data, indent=4)))
        except Exception:
            print(msg, str(data))



class ASMPolicyManager:
    @staticmethod
    def diffPolicies(srcAssetId: int, dstAssetId: int, srcPolicyId: str, dstPolicyId: str) -> dict:
        try:
            return Client().get(
                "/api/v1/f5/source-asset/" + str(srcAssetId) + "/destination-asset/" + str(
                    dstAssetId) + "/asm/source-policy/" + srcPolicyId + "/destination-policy/" + dstPolicyId + "/differences/"
            ).json()
        except Exception as e:
            print(e.args)



    @staticmethod
    def mergePolicies(dstAssetId: int, diffReference: str, diffIds: list = None) -> dict:
        diffIds = diffIds or []

        try:
            return Client().put(
                path=f"/api/v1/f5/{dstAssetId}/asm/policy-diff/{diffReference}/merge/",
                data={
                    "data": {
                        "diff-ids": diffIds,
                    }
                },
                content_type="application/json"
            ).json()

        except Exception as e:
            print(e.args)



    @staticmethod
    def listPolicies(assetId):
        try:
            return Client().get(f"/api/v1/f5/{assetId}/asm/policies/").json()
        except Exception as e:
            print(e.args)



########################################################################################################################
# Main
########################################################################################################################

try:
    disable_warnings(InsecureRequestWarning)
    django.setup()

    # Load user-inserted assets.
    Asset.loadAsset(ip=srcIpAsset, user=srcUser, passwd=srcPasswd, environment="src")
    Asset.loadAsset(ip=dstIpAsset, user=dstUser, passwd=dstPasswd, environment="dst")
    Util.log(Asset.listAssets(), "Assets loaded: ")

    # Fetch policies' differences.
    diffData = ASMPolicyManager.diffPolicies(srcAssetId=1, srcPolicyId="K-78hGsC0JAvnuDbF1Vh2A", dstAssetId=2, dstPolicyId="9n2I7YaXBn94jfKETtsidA")["data"]
    for diffEntityType, diffList in diffData["differences"].items():
        print("#######################")
        print("Diff type: " + diffEntityType + "\n\n")

        for el in diffList:
            print("Entity name: " + el["entityName"] + "\n")
            print("Diff type: " + el["diffType"] + "\n")
            a = input("Merge diff for entity?(y/n)\n")
            if a == "y":
                print(a + "\n")
            else:
                print("stoca\n")

except KeyError:
    pass
except Exception as ex:
    Util.log(ex.args)
finally:
    Asset.purgeAssets()
