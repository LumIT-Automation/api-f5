from rest_framework import serializers


class F5VirtualServerSerializer(serializers.Serializer):
    class F5VirtualServerInnerSerializer(serializers.Serializer):
        class F5VirtualServerPoolReferenceSerializer(serializers.Serializer):
            link = serializers.CharField(max_length=255, required=True)

        class F5VirtualServerSourceAddressTranslationSerializer(serializers.Serializer):
            type = serializers.CharField(max_length=255, required=True)

        class F5VirtualServerSecurityLogProfilesReferenceSerializer(serializers.Serializer):
            link = serializers.CharField(max_length=255, required=True)

        class F5VirtualServerPersistSerializer(serializers.Serializer):
            class F5VirtualServerPersistNameReferenceSerializer(serializers.Serializer):
                link = serializers.CharField(max_length=255, required=True)

            name = serializers.CharField(max_length=255, required=True)
            partition = serializers.CharField(max_length=255, required=True)
            tmDefault = serializers.CharField(max_length=255, required=True)
            nameReference = F5VirtualServerPersistNameReferenceSerializer(required=True)

        class F5VirtualServerReferenceSerializer(serializers.Serializer):
            link = serializers.CharField(max_length=255, required=True)
            isSubcollection = serializers.BooleanField(required=True)

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
        destination = serializers.CharField(max_length=255, required=True)
        enabled = serializers.BooleanField(required=False)
        gtmScore = serializers.IntegerField(required=False)
        ipProtocol = serializers.CharField(max_length=255, required=False)
        lastModifiedTime = serializers.CharField(max_length=255, required=False)
        mask = serializers.CharField(max_length=255, required=True)
        mirror = serializers.CharField(max_length=255, required=False)
        mobileAppTunnel = serializers.CharField(max_length=255, required=False)
        nat64 = serializers.CharField(max_length=255, required=False)
        pool = serializers.CharField(max_length=255, required=True)
        poolReference = F5VirtualServerPoolReferenceSerializer(required=False)
        rateLimit = serializers.CharField(max_length=255, required=False)
        rateLimitDstMask = serializers.IntegerField(required=False)
        rateLimitMode = serializers.CharField(max_length=255, required=False)
        rateLimitSrcMask = serializers.IntegerField(required=False)
        serviceDownImmediateAction = serializers.CharField(max_length=255, required=False)
        source = serializers.CharField(max_length=255, required=True)
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

        profiles = serializers.CharField(max_length=255, required=False)

    data = F5VirtualServerInnerSerializer(required=True)
