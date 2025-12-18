from rest_framework import serializers


class F5InterfacesSerializer(serializers.Serializer):
    class F5InterfacesItemsSerializer(serializers.Serializer):
        class F5InterfacesValidatorsSerializer(serializers.Serializer):
            link = serializers.CharField(max_length=255, required=False)

        assetId = serializers.IntegerField(required=False)
        name = serializers.CharField(max_length=255, required=True)
        partition = serializers.CharField(max_length=255, required=False)
        fullPath = serializers.CharField(max_length=255, required=False)
        generation = serializers.IntegerField(required=False)
        id = serializers.IntegerField(required=False)
        connectionLimit = serializers.IntegerField(required=False)
        selfLink = serializers.CharField(max_length=255, required=False)
        strict = serializers.CharField(max_length=255, required=False)

        bundle = serializers.CharField(max_length=255, required=False)
        bundleSpeed = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(max_length=255, required=False)

        flowControl = serializers.CharField(max_length=255, required=False)
        forceGigabitFiber = serializers.CharField(max_length=255, required=False)
        forwardErrorCorrection = serializers.CharField(max_length=255, required=False)
        ifAlias = serializers.CharField(max_length=255, required=False)
        lldpAdmin = serializers.CharField(max_length=255, required=False)
        macAddress = serializers.CharField(max_length=255, required=False)
        media = serializers.CharField(max_length=255, required=False)
        mediaActive = serializers.CharField(max_length=255, required=False)
        mediaFixed = serializers.CharField(max_length=255, required=False)
        mediaMax = serializers.CharField(max_length=255, required=False)
        mediaSfp = serializers.CharField(max_length=255, required=False)
        moduleDescription = serializers.CharField(max_length=255, required=False)
        portFwdMode = serializers.CharField(max_length=255, required=False)
        preferPort = serializers.CharField(max_length=255, required=False)
        qinqEthertype = serializers.CharField(max_length=255, required=False)
        serial = serializers.CharField(max_length=255, required=False)
        stp = serializers.CharField(max_length=255, required=False)
        stpAutoEdgePort = serializers.CharField(max_length=255, required=False)
        stpEdgePort = serializers.CharField(max_length=255, required=False)
        stpLinkType = serializers.CharField(max_length=255, required=False)
        vendor = serializers.CharField(max_length=255, required=False)
        vendorOui = serializers.CharField(max_length=255, required=False)
        vendorPartnum = serializers.CharField(max_length=255, required=False)
        vendorRevision = serializers.CharField(max_length=255, required=False)

        ifIndex = serializers.IntegerField(required=False)
        lldpTlvmap = serializers.IntegerField(required=False)
        mtu = serializers.IntegerField(required=False)

        disabled = serializers.BooleanField(required=False)
        enabled = serializers.BooleanField(required=False)
        stpReset = serializers.BooleanField(required=False)

    items = F5InterfacesItemsSerializer(many=True)
