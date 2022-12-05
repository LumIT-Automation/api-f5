#!/usr/bin/python3

import os
import argparse
import sqlite3

import django
from django.conf import settings
from django.test import Client


####################
parser = argparse.ArgumentParser()
parser.add_argument('-a','--src_asset',help='Source asset of the policies (ip/hostname)',required=True)
parser.add_argument('-A','--dst_asset',help='Destination asset of the policies (ip/hostname)',required=True)
parser.add_argument('-u','--src_user',help='Source asset username (default: admin)',required=False)
parser.add_argument('-U','--dst_user',help='Destination asset username (default: admin)',required=False)
parser.add_argument('-p','--src_passwd',help='Source asset password',required=False)
parser.add_argument('-P','--dst_passwd',help='Destination asset password',required=False)
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


####################
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


def loadAsset(ip: str, user: str, passwd: str):
    baseUrl = "https://" + ip + "/mgmt/"
    try:
        return Client().post(
                path = '/api/v1/f5/assets/',
                data = {
                    "data": {
                        "address": ip,
                        "fqdn": ip,
                        "baseurl": baseUrl,
                        "tlsverify": 0,
                        "datacenter": "",
                        "environment": "src",
                        "position": "",
                        "username": user,
                        "password": passwd
                    }
                },
                content_type = "application/json"
        )

    except Exception as e:
        print(e.args)



def listAsset():
    try:
        return Client().get('/api/v1/f5/assets/').json()
    except Exception as e:
        print(e.args)



def deleteAsset(assetId):
    url = '/api/v1/f5/asset/' + str(assetId) + '/'
    try:
        return Client().delete(url)
    except Exception as e:
        print(e.args)


# To reset the autoincrement number try this shell command:
# echo "UPDATE sqlite_sequence SET seq=0 WHERE name='asset';" | sqlite3 f5.db
def purgeAssets():
    try:
        assetsList = listAsset()["data"]["items"]
        for asset in assetsList:
            deleteAsset(asset["id"])

        # Todo: use django db connector
        """
        # Reset the autoincrement values for the table asset.
        dbConn = sqlite3.connect("/var/www/api/f5.db")
        cursor = dbConn.cursor()
        cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name='asset'")
        """
    except KeyError:
        pass
    except Exception as e:
        print(e.args)



def listPolicies(assetId):
    url = '/api/v1/f5/' + str(assetId) + '/asm/policies/'
    try:
        return Client().get(url).json()
    except Exception as e:
        print(e.args)



def getPolicy(assetId, policyId):
    url = '/api/v1/f5/' + str(assetId) + '/asm/policy/' + policyId + '/'
    try:
        return Client().get(url).json()
    except Exception as e:
        print(e.args)



def diffPolicy(srcAssetId: int, dstAssetId: int, srcPolicyId: str, dstPolicyId: str):
    url = '/api/v1/f5/' + str(srcAssetId) + '/' + str(dstAssetId) + '/asm/source-policy/' + srcPolicyId + '/destination-policy/' + dstPolicyId + '/differences/'
    try:
        return Client().get(url).json()
    except Exception as e:
        print(e.args)



def mergePolicy(dstAssetId: int, dstPolicyId: str, diffReference: str):
    url = '/api/v1/f5/' + str(dstAssetId) + '/asm/policy/' + dstPolicyId + '/merge/'
    try:
        return Client().put(
                path = url,
                data = { "data": {
                    "diff-reference": diffReference,
                    "entity-type": []
                }},
                content_type = "application/json"
        )

    except Exception as e:
        print(e.args)


####################
django.setup()


loadAsset(ip=srcIpAsset, user=srcUser, passwd=srcPasswd)
loadAsset(ip=dstIpAsset, user=dstUser, passwd=dstPasswd)
print("Assets loaded:")
print(listAsset())

print('#################')
print('Policies on source asset:')
#print(listPolicies(1))
print('#################')

print('POLICY on ASSET 2')
#print(getPolicy(2, 'uIGB1pBIcH8WprjX8KBR0w'))
print('#################')

print('MERGE POLICY on ASSET 2')
#print(mergePolicy(srcAssetId=1, dstAssetId=2, srcPolicyId='K-78hGsC0JAvnuDbF1Vh2A',  dstPolicyId='9n2I7YaXBn94jfKETtsidA'))
print('#################')

purgeAssets()
print("Assets cleaned up")
#print(listAsset())
