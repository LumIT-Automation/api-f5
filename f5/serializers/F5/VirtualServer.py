from rest_framework import serializers

from f5.serializers.F5.Policy import F5PolicySerializer
from f5.serializers.F5.Profile import F5ProfileSerializer


class F5VirtualServerSerializer(serializers.Serializer):
    class F5VirtualServerPoolReferenceSerializer(serializers.Serializer):
        link = serializers.CharField(max_length=255, required=False)

    class F5VirtualServerSourceAddressTranslationSerializer(serializers.Serializer):
        type = serializers.CharField(max_length=255, required=False)
        pool = serializers.CharField(max_length=255, required=False)

    class F5VirtualServerSecurityLogProfilesReferenceSerializer(serializers.Serializer):
        link = serializers.CharField(max_length=255, required=False)

    class F5VirtualServerPersistSerializer(serializers.Serializer):
        class F5VirtualServerPersistNameReferenceSerializer(serializers.Serializer):
            link = serializers.CharField(max_length=255, required=False)

        name = serializers.CharField(max_length=255, required=False)
        partition = serializers.CharField(max_length=255, required=False)
        tmDefault = serializers.CharField(max_length=255, required=False)
        nameReference = F5VirtualServerPersistNameReferenceSerializer(required=False)

    class F5VirtualServerReferenceSerializer(serializers.Serializer):
        link = serializers.CharField(max_length=255, required=False)
        isSubcollection = serializers.BooleanField(required=False)

    class F5VirtualServersRulesReferenceSerializer(serializers.Serializer):
        link = serializers.CharField(max_length=255, required=False)

    assetId = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=True)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=255, required=False)
    addressStatus = serializers.CharField(max_length=255, required=False)
    autoLasthop = serializers.CharField(max_length=255, required=False)
    cmpEnabled = serializers.CharField(max_length=255, required=False)
    connectionLimit = serializers.IntegerField(required=False)
    creationTime = serializers.CharField(max_length=255, required=False)
    destination = serializers.CharField(max_length=255, required=False)
    enabled = serializers.BooleanField(required=False)
    evictionProtected = serializers.CharField(max_length=255, required=False)
    gtmScore = serializers.IntegerField(required=False)
    ipProtocol = serializers.CharField(max_length=255, required=False)
    lastModifiedTime = serializers.CharField(max_length=255, required=False)
    mask = serializers.RegexField(
        regex='(^(((255\.){3}(255|254|252|248|240|224|192|128|0+))|((255\.){2}(255|254|252|248|240|224|192|128|0+)\.0)|((255\.)(255|254|252|248|240|224|192|128|0+)(\.0+){2})|((255|254|252|248|240|224|192|128|0+)(\.0+){3}))$|any|any4|any6)',
        required=True
    )
    mirror = serializers.CharField(max_length=255, required=False)
    mobileAppTunnel = serializers.CharField(max_length=255, required=False)
    nat64 = serializers.CharField(max_length=255, required=False)
    pool = serializers.CharField(max_length=255, required=False)
    serversslUseSni = serializers.CharField(max_length=255, required=False)
    poolReference = F5VirtualServerPoolReferenceSerializer(required=False)
    rateLimit = serializers.CharField(max_length=255, required=False)
    rateLimitDstMask = serializers.IntegerField(required=False)
    rateLimitMode = serializers.CharField(max_length=255, required=False)
    rateLimitSrcMask = serializers.IntegerField(required=False)
    serviceDownImmediateAction = serializers.CharField(max_length=255, required=False)
    source = serializers.CharField(max_length=255, required=False)
    sourceAddressTranslation = F5VirtualServerSourceAddressTranslationSerializer(required=True)
    sourcePort = serializers.CharField(max_length=255, required=False)
    synCookieStatus = serializers.CharField(max_length=255, required=False)
    translateAddress = serializers.CharField(max_length=255, required=False)
    translatePort = serializers.CharField(max_length=255, required=False)
    vlansDisabled = serializers.BooleanField(required=False)
    vsIndex = serializers.IntegerField(required=False)
    securityLogProfiles = serializers.ListField(
        child=serializers.CharField(max_length=255, required=True),
        required=False
    )
    securityLogProfilesReference = F5VirtualServerSecurityLogProfilesReferenceSerializer(many=True, required=False)
    persist = F5VirtualServerPersistSerializer(many=True, required=False)
    policiesReference = F5VirtualServerReferenceSerializer(required=False)
    profilesReference = F5VirtualServerReferenceSerializer(required=False)
    rulesReference = F5VirtualServersRulesReferenceSerializer(many=True, required=False)

    policies = F5PolicySerializer(many=True, required=False)
    profiles = F5ProfileSerializer(many=True, required=False)
    rules = serializers.ListField(
        child=serializers.CharField(max_length=255, required=False),
        required=False
    )
