import re
import json
import time
import xmltodict
from datetime import datetime

from typing import List, Dict

from f5.models.F5.Asset.Asset import Asset
from f5.models.F5.ASM.backend.PolicyBase import PolicyBase

from f5.helpers.ApiSupplicant import ApiSupplicant
from f5.helpers.Exception import CustomException
from f5.helpers.Log import Log


class PolicyDiffManager(PolicyBase):

    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def createDiff(assetId: int, destinationPolicyId: str, firstPolicy: str) -> str:
        diffReference = ""
        timeout = 3600 # [second]

        try:
            f5 = Asset(assetId)

            # Create policies' differences.
            api = ApiSupplicant(
                endpoint=f5.baseurl + "tm/asm/tasks/policy-diff/",
                auth=(f5.username, f5.password),
                tlsVerify=f5.tlsverify
            )

            taskInformation = api.post(
                additionalHeaders={
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "firstPolicyReference": {
                        "link": "https://localhost/mgmt/tm/asm/policies/" + destinationPolicyId
                    },
                    "secondPolicyReference": {
                        "link": firstPolicy
                    }
                })
            )["payload"]

            PolicyDiffManager._log(
                f"[AssetID: {assetId}] Creating differences between {destinationPolicyId} and {firstPolicy}..."
            )

            # Monitor export file creation (async tasks).
            t0 = time.time()

            while True:
                try:
                    api = ApiSupplicant(
                        endpoint=f5.baseurl + "tm/asm/tasks/policy-diff/" + taskInformation["id"] + "/",
                        auth=(f5.username, f5.password),
                        tlsVerify=f5.tlsverify
                    )

                    PolicyDiffManager._log(
                        f"[AssetID: {assetId}] Waiting for task to complete..."
                    )

                    taskOutput = api.get()["payload"]
                    taskStatus = taskOutput["status"].lower()
                    if taskStatus == "completed":
                        result = taskOutput.get("result", {})
                        PolicyDiffManager._log(
                            f"[AssetID: {assetId}] Differences' result: {result}"
                        )

                        matches = re.search(r"(?<=diffs\/)(.*)(?=\?)", result.get("policyDiffReference", {}).get("link", ""))
                        if matches:
                            diffReference = str(matches.group(1)).strip()

                        return diffReference
                    if taskStatus == "failure":
                        raise CustomException(status=400, payload={"F5": f"policy diff failed"})

                    if time.time() >= t0 + timeout: # timeout reached.
                        raise CustomException(status=400, payload={"F5": f"policy diff times out"})

                    time.sleep(30)
                except KeyError:
                    raise CustomException(status=400, payload={"F5": f"policy diff failed"})
        except Exception as e:
            raise e



    @staticmethod
    def listDifferences(sourceAssetId: int, sourcePolicyId: str, destinationAssetId: int, diffReferenceId: str, sourcePolicyXML: str) -> dict:
        page = 0
        items = 100
        differences = []

        PolicyDiffManager._log(
            f"[AssetID: {destinationAssetId}] Downloading and parsing differences for {diffReferenceId}..."
        )

        try:
            f5 = Asset(destinationAssetId)

            while True:
                # Collect all differences - request must be paginated.
                skip = items * page

                api = ApiSupplicant(
                    endpoint=f5.baseurl + "tm/asm/policy-diffs/" + diffReferenceId + "/differences/?$skip="+str(skip)+"&$top="+str(items),
                    auth=(f5.username, f5.password),
                    tlsVerify=f5.tlsverify,
                    silent=True
                )

                response = api.get()["payload"]
                differences.extend(
                    PolicyDiffManager.__cleanupDifferences(
                        response.get("items", [])
                    )
                )

                if int(response.get("pageIndex", 0)) == int(response.get("totalPages", 0)):
                    break
                else:
                    page += 1

            completeDifferences = PolicyDiffManager.__differencesAddSourceObjectDate(
                PolicyDiffManager.__differencesOrderByType(differences),
                sourcePolicyXML,
                sourceAssetId,
                sourcePolicyId
            )

            return completeDifferences
        except Exception as e:
            raise e



    ####################################################################################################################
    # Private static methods
    ####################################################################################################################

    @staticmethod
    def __cleanupDifferences(differences: list) -> list:
        diffs = []

        try:
            for el in differences:
                diffs.append({
                    "id": el["id"],
                    "entityType": el["entityKind"].split(":")[3],
                    "diffType": el["diffType"],
                    "firstLastUpdateMicros": el["firstLastUpdateMicros"],
                    "details": el.get("details", []),
                    "entityName": el["entityName"],
                    "canMergeSecondToFirst": el["canMergeSecondToFirst"],
                    "canMergeFirstToSecond": el["canMergeFirstToSecond"],
                })

            return diffs
        except IndexError:
            pass
        except Exception as e:
            raise e



    @staticmethod
    def __differencesOrderByType(differences: list) -> dict:
        diffs: Dict[str, List[dict]] = {}

        try:

            for el in differences:
                entityType = el["entityType"]
                if entityType not in diffs:
                    diffs[entityType] = []

                del(el["entityType"])
                diffs[entityType].append(el)

            return diffs
        except Exception as e:
            raise e



    @staticmethod
    def __toEpoch(isoformat: str):
        try:
            e = int(datetime.strptime(isoformat, "%Y-%m-%dT%H:%M:%SZ").timestamp())
        except Exception:
            e = 0

        return e



    @staticmethod
    def __differencesAddSourceObjectDate(differences: dict, sourcePolicyXML: str, sourceAssetId: int, sourcePolicyId: str) -> dict:
        try:
            f5 = Asset(sourceAssetId)
            xml = xmltodict.parse(sourcePolicyXML)

            for k, v in differences.items():
                # Some last modify timestamps are contained within the XML file.
                if k == "filetypes":
                    xmlParameters: List[dict] = xml.get("policy").get("file_types").get("file_type")
                    for el in v:
                        try:
                            # Read date from xml data, for corresponding object name.
                            el["secondLastUpdateMicros"] = PolicyDiffManager.__toEpoch(
                                list(filter(lambda i: i["@name"] == el["entityName"], xmlParameters))[0]["last_updated"]
                            )
                        except Exception:
                            el["secondLastUpdateMicros"] = 0

                elif k == "parameters":
                    xmlParameters: List[dict] = xml.get("policy").get("parameters").get("parameter")
                    for el in v:
                        try:
                            el["secondLastUpdateMicros"] = PolicyDiffManager.__toEpoch(
                                list(filter(lambda i: i["@name"] == el["entityName"], xmlParameters))[0]["last_updated"]
                            )
                        except Exception:
                            el["secondLastUpdateMicros"] = 0

                elif k == "urls":
                    xmlParameters: List[dict] = xml.get("policy").get("urls").get("url")
                    for el in v:
                        try:
                            el["secondLastUpdateMicros"] = PolicyDiffManager.__toEpoch(
                                list(filter(lambda i: "[" + i["@protocol"] + "] " + i["@name"] == el["entityName"], xmlParameters))[0]["last_updated"]
                            )
                        except Exception:
                            el["secondLastUpdateMicros"] = 0

                else:
                    # For all the other timestamps, callbacks to source policy are needed.
                    # @todo: create models.
                    # @stub.
                    for el in v:
                        el["secondLastUpdateMicros"] = 0

                    try:
                        api = ApiSupplicant(
                            endpoint=f5.baseurl + "tm/asm/policies/" + sourcePolicyId + "/cookies/",
                            auth=(f5.username, f5.password),
                            tlsVerify=f5.tlsverify
                        )

                        o = api.get()["payload"]
                    except Exception as e:
                        raise e

            return differences
        except Exception as e:
            raise e

        # {
        #             "signatureRequirementReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/signature-requirements"
        #             },
        #
        #             "plainTextProfileReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/plain-text-profiles"
        #             },
        #
        #             "behavioralEnforcementReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/behavioral-enforcement?"
        #             },
        #
        #             "dataGuardReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/data-guard?"
        #             },
        #
        #             "databaseProtectionReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/database-protection?"
        #             },
        #
        #             "cookieSettingsReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/cookie-settings?"
        #             },
        #
        #             "csrfUrlReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/csrf-urls"
        #             },
        #
        #             "headerSettingsReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/header-settings?"
        #             },
        #
        #             "sectionReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/sections"
        #             },
        #
        #             "flowReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/flows"
        #             },
        #
        #             "loginPageReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/login-pages"
        #             },
        #
        #             "policyBuilderParameterReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/policy-builder-parameter?"
        #             },
        #
        #             "threatCampaignReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/threat-campaigns"
        #             },
        #
        #             "csrfProtectionReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/csrf-protection?"
        #             },
        #
        #             "graphqlProfileReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/graphql-profiles"
        #             },
        #
        #             "policyAntivirusReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/antivirus?"
        #             },
        #
        #             "policyBuilderCookieReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/policy-builder-cookie?"
        #             },
        #
        #             "ipIntelligenceReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/ip-intelligence?"
        #             },
        #
        #             "sessionAwarenessSettingsReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/session-tracking?"
        #             },
        #
        #             "policyBuilderUrlReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/policy-builder-url?"
        #             },
        #
        #             "policyBuilderServerTechnologiesReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/policy-builder-server-technologies?"
        #             },
        #
        #             "policyBuilderFiletypeReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/policy-builder-filetype?"
        #             },
        #
        #             "signatureSetReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/signature-sets"
        #             },
        #
        #             "parameterReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/parameters"
        #             },
        #
        #             "loginEnforcementReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/login-enforcement?"
        #             },
        #
        #             "openApiFileReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/open-api-files"
        #             },
        #
        #             "navigationParameterReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/navigation-parameters"
        #             },
        #
        #             "gwtProfileReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/gwt-profiles"
        #             },
        #
        #             "webhookReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/webhooks"
        #             },
        #
        #             "whitelistIpReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/whitelist-ips"
        #             },
        #
        #             "historyRevisionReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/history-revisions"
        #             },
        #
        #             "policyBuilderReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/policy-builder?"
        #             },
        #
        #             "responsePageReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/response-pages"
        #             },
        #
        #             "vulnerabilityAssessmentReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/vulnerability-assessment?"
        #             },
        #
        #             "serverTechnologyReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/server-technologies"
        #             },
        #
        #             "cookieReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/cookies"
        #             },
        #
        #             "blockingSettingReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/blocking-settings"
        #             },
        #
        #             "hostNameReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/host-names"
        #             },
        #
        #             "threatCampaignSettingReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/threat-campaign-settings?"
        #             },
        #
        #             "signatureReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/signatures"
        #             },
        #
        #             "policyBuilderRedirectionProtectionReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/policy-builder-redirection-protection?"
        #             },
        #
        #             "filetypeReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/filetypes"
        #             },
        #
        #             "ssrfHostReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/ssrf-hosts"
        #             },
        #
        #             "sessionTrackingStatusReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/session-tracking-statuses"
        #             },
        #
        #             "auditLogReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/audit-logs"
        #             },
        #
        #             "disallowedGeolocationReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/disallowed-geolocations"
        #             },
        #
        #             "redirectionProtectionDomainReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/redirection-protection-domains"
        #             },
        #
        #             "signatureSettingReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/signature-settings?"
        #             },
        #
        #             "deceptionResponsePageReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/deception-response-pages"
        #             },
        #
        #             "websocketUrlReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/websocket-urls"
        #             },
        #
        #             "xmlProfileReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/xml-profiles"
        #             },
        #
        #             "methodReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/methods"
        #             },
        #
        #             "vulnerabilityReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/vulnerabilities"
        #             },
        #
        #             "redirectionProtectionReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/redirection-protection?"
        #             },
        #
        #             "policyBuilderSessionsAndLoginsReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/policy-builder-sessions-and-logins?"
        #             },
        #
        #             "templateReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policy-templates/EzpBNMs9gbVsF5uuiBjYDw"
        #             },
        #
        #             "policyBuilderHeaderReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/policy-builder-header?"
        #             },
        #
        #             "urlReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/urls"
        #             },
        #
        #             "headerReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/headers"
        #             },
        #
        #             "actionItemReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/action-items"
        #             },
        #
        #             "microserviceReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/microservices"
        #             },
        #
        #             "xmlValidationFileReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/xml-validation-files"
        #             },
        #
        #             "jsonProfileReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/json-profiles"
        #             },
        #
        #             "bruteForceAttackPreventionReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/brute-force-attack-preventions"
        #             },
        #
        #             "disabledActionItemReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/disabled-action-items"
        #             },
        #
        #             "jsonValidationFileReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/json-validation-files"
        #             },
        #
        #             "extractionReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/extractions"
        #             },
        #
        #             "characterSetReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/character-sets"
        #             },
        #
        #             "suggestionReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/suggestions"
        #             },
        #
        #             "deceptionSettingsReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/deception-settings?"
        #             },
        #
        #             "sensitiveParameterReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/sensitive-parameters"

        #             },
        #             "generalReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/general?"
        #             },
        #
        #             "policyBuilderCentralConfigurationReference": {
        #                 "link": "https://localhost/mgmt/tm/asm/policies/K-78hGsC0JAvnuDbF1Vh2A/policy-builder-central-configuration?"
        #             }
