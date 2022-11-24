from typing import List, Dict, Union

from f5.models.F5.ASM.backend.Policy import Policy as Backend


Link: Dict[str, str] = {
    "link": ""
}

RulesReference: Dict[str, Union[str, bool]] = {
    "link": "",
    "isSubcollection": False
}

class Policy:
    def __init__(self, assetId: int, id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.id: str = id

        #         "signatureRequirementReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/signature-requirements?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "plainTextProfileReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/plain-text-profiles?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "enablePassiveMode": false,
        #         "behavioralEnforcementReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/behavioral-enforcement?ver=16.1.0"
        #         },
        #         "dataGuardReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/data-guard?ver=16.1.0"
        #         },
        #         "createdDatetime": "2022-10-03T14:47:28Z",
        #         "databaseProtectionReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/database-protection?ver=16.1.0"
        #         },
        #         "cookieSettingsReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/cookie-settings?ver=16.1.0"
        #         },
        #         "csrfUrlReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/csrf-urls?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "versionLastChange": "Policy Building Settings Policy Building Settings [update]: Fully Automatic was set to 1. { audit: policy = /Common/test_0310, username = admin, client IP = 10.41.173.140 }",
        #         "name": "test_0310",
        #         "caseInsensitive": false,
        #         "headerSettingsReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/header-settings?ver=16.1.0"
        #         },
        #         "sectionReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/sections?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "flowReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/flows?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "loginPageReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/login-pages?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "description": "Rapid Deployment Policy",
        #         "fullPath": "/Common/test_0310",
        #         "policyBuilderParameterReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/policy-builder-parameter?ver=16.1.0"
        #         },
        #         "hasParent": false,
        #         "threatCampaignReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/threat-campaigns?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "partition": "Common",
        #         "managedByBewaf": false,
        #         "csrfProtectionReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/csrf-protection?ver=16.1.0"
        #         },
        #         "graphqlProfileReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/graphql-profiles?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "policyAntivirusReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/antivirus?ver=16.1.0"
        #         },
        #         "kind": "tm:asm:policies:policystate",
        #         "virtualServers": [],
        #         "policyBuilderCookieReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/policy-builder-cookie?ver=16.1.0"
        #         },
        #         "ipIntelligenceReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/ip-intelligence?ver=16.1.0"
        #         },
        #         "protocolIndependent": false,
        #         "sessionAwarenessSettingsReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/session-tracking?ver=16.1.0"
        #         },
        #         "policyBuilderUrlReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/policy-builder-url?ver=16.1.0"
        #         },
        #         "policyBuilderServerTechnologiesReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/policy-builder-server-technologies?ver=16.1.0"
        #         },
        #         "policyBuilderFiletypeReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/policy-builder-filetype?ver=16.1.0"
        #         },
        #         "signatureSetReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/signature-sets?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "parameterReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/parameters?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "applicationLanguage": "utf-8",
        #         "enforcementMode": "transparent",
        #         "loginEnforcementReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/login-enforcement?ver=16.1.0"
        #         },
        #         "openApiFileReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/open-api-files?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "navigationParameterReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/navigation-parameters?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "gwtProfileReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/gwt-profiles?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "webhookReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/webhooks?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "whitelistIpReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/whitelist-ips?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "historyRevisionReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/history-revisions?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "policyBuilderReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/policy-builder?ver=16.1.0"
        #         },
        #         "responsePageReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/response-pages?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "vulnerabilityAssessmentReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/vulnerability-assessment?ver=16.1.0"
        #         },
        #         "serverTechnologyReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/server-technologies?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "cookieReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/cookies?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "blockingSettingReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/blocking-settings?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "hostNameReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/host-names?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "versionDeviceName": "f5labpri.lumitlab.internal",
        #         "selfLink": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w?ver=16.1.0",
        #         "threatCampaignSettingReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/threat-campaign-settings?ver=16.1.0"
        #         },
        #         "signatureReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/signatures?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "policyBuilderRedirectionProtectionReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/policy-builder-redirection-protection?ver=16.1.0"
        #         },
        #         "filetypeReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/filetypes?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "id": "uIGB1pBIcH8WprjX8KBR0w",
        #         "modifierName": "",
        #         "manualVirtualServers": [],
        #         "versionDatetime": "2022-10-03T14:47:31Z",
        #         "ssrfHostReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/ssrf-hosts?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "subPath": "/Common",
        #         "sessionTrackingStatusReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/session-tracking-statuses?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "active": false,
        #         "auditLogReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/audit-logs?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "disallowedGeolocationReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/disallowed-geolocations?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "redirectionProtectionDomainReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/redirection-protection-domains?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "type": "security",
        #         "signatureSettingReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/signature-settings?ver=16.1.0"
        #         },
        #         "deceptionResponsePageReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/deception-response-pages?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "websocketUrlReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/websocket-urls?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "xmlProfileReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/xml-profiles?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "methodReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/methods?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "vulnerabilityReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/vulnerabilities?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "redirectionProtectionReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/redirection-protection?ver=16.1.0"
        #         },
        #         "policyBuilderSessionsAndLoginsReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/policy-builder-sessions-and-logins?ver=16.1.0"
        #         },
        #         "templateReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policy-templates/EzpBNMs9gbVsF5uuiBjYDw?ver=16.1.0",
        #             "title": "Rapid Deployment Policy"
        #         },
        #         "policyBuilderHeaderReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/policy-builder-header?ver=16.1.0"
        #         },
        #         "creatorName": "admin",
        #         "urlReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/urls?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "headerReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/headers?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "actionItemReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/action-items?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "microserviceReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/microservices?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "xmlValidationFileReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/xml-validation-files?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "lastUpdateMicros": 0,
        #         "jsonProfileReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/json-profiles?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "bruteForceAttackPreventionReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/brute-force-attack-preventions?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "disabledActionItemReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/disabled-action-items?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "jsonValidationFileReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/json-validation-files?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "extractionReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/extractions?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "characterSetReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/character-sets?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "suggestionReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/suggestions?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "deceptionSettingsReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/deception-settings?ver=16.1.0"
        #         },
        #         "isModified": false,
        #         "sensitiveParameterReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/sensitive-parameters?ver=16.1.0",
        #             "isSubCollection": true
        #         },
        #         "generalReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/general?ver=16.1.0"
        #         },
        #         "versionPolicyName": "/Common/test_0310",
        #         "policyBuilderCentralConfigurationReference": {
        #             "link": "https://localhost/mgmt/tm/asm/policies/uIGB1pBIcH8WprjX8KBR0w/policy-builder-central-configuration?ver=16.1.0"
        #         },
        #         "assetId": 2



    ####################################################################################################################
    # Public methods
    ####################################################################################################################

    def info(self) -> dict:
        try:
            i = Backend.info(self.assetId, self.id)
            i["assetId"] = self.assetId

            return i
        except Exception as e:
            raise e



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def list(assetId: int) -> List[dict]:
        try:
            l = Backend.list(assetId)
            for el in l:
                el["assetId"] = assetId

            return l
        except Exception as e:
            raise e



    @staticmethod
    def importPolicy(assetId: int, policyId: str):
        try:
            return Backend.downloadPolicy(
                assetId,
                Backend.createExportFile(assetId, policyId)
            )
        except Exception as e:
            raise e
