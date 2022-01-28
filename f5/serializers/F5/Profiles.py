from rest_framework import serializers


class F5ProfilesSerializer(serializers.Serializer):
    class F5ProfilesItemsSerializer(serializers.Serializer):
        class F5ProfilesReferenceSerializer(serializers.Serializer):
            link = serializers.CharField(max_length=255, required=True)

        name = serializers.CharField(max_length=255, required=True)
        partition = serializers.CharField(max_length=255, required=True)
        fullPath = serializers.CharField(max_length=255, required=True)
        generation = serializers.IntegerField(required=False)
        selfLink = serializers.CharField(max_length=255, required=True)
        defaultsFrom = serializers.CharField(max_length=255, required=False)
        defaultsFromReference = F5ProfilesReferenceSerializer(required=False)
        clientTimeout = serializers.IntegerField(required=False)
        ipTtlV4 = serializers.IntegerField(required=False)
        ipTtlV6 = serializers.IntegerField(required=False)
        mssOverride = serializers.IntegerField(required=False)
        otherPvaClientpktsThreshold = serializers.IntegerField(required=False)
        otherPvaServerpktsThreshold = serializers.IntegerField(required=False)
        pvaDynamicClientPackets = serializers.IntegerField(required=False)
        pvaDynamicServerPackets = serializers.IntegerField(required=False)
        receiveWindowSize = serializers.IntegerField(required=False)
        synCookieMss = serializers.IntegerField(required=False)
        tcpTimeWaitTimeout = serializers.IntegerField(required=False)
        appService = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(max_length=255, required=False)
        explicitFlowMigration = serializers.CharField(max_length=255, required=False)
        hardwareSynCookie = serializers.CharField(max_length=255, required=False)
        idleTimeout = serializers.CharField(max_length=255, required=False)
        ipDfMode = serializers.CharField(max_length=255, required=False)
        ipTosToClient = serializers.CharField(max_length=255, required=False)
        ipTosToServer = serializers.CharField(max_length=255, required=False)
        ipTtlMode = serializers.CharField(max_length=255, required=False)
        keepAliveInterval = serializers.CharField(max_length=255, required=False)
        lateBinding = serializers.CharField(max_length=255, required=False)
        linkQosToClient = serializers.CharField(max_length=255, required=False)
        linkQosToServer = serializers.CharField(max_length=255, required=False)
        looseClose = serializers.CharField(max_length=255, required=False)
        looseInitialization = serializers.CharField(max_length=255, required=False)
        otherPvaOffloadDirection = serializers.CharField(max_length=255, required=False)
        otherPvaWhentoOffload = serializers.CharField(max_length=255, required=False)
        priorityToClient = serializers.CharField(max_length=255, required=False)
        priorityToServer = serializers.CharField(max_length=255, required=False)
        pvaAcceleration = serializers.CharField(max_length=255, required=False)
        pvaFlowAging = serializers.CharField(max_length=255, required=False)
        pvaFlowEvict = serializers.CharField(max_length=255, required=False)
        pvaOffloadDynamic = serializers.CharField(max_length=255, required=False)
        pvaOffloadState = serializers.CharField(max_length=255, required=False)
        reassembleFragments = serializers.CharField(max_length=255, required=False)
        resetOnTimeout = serializers.CharField(max_length=255, required=False)
        rttFromClient = serializers.CharField(max_length=255, required=False)
        rttFromServer = serializers.CharField(max_length=255, required=False)
        serverSack = serializers.CharField(max_length=255, required=False)
        serverTimestamp = serializers.CharField(max_length=255, required=False)
        softwareSynCookie = serializers.CharField(max_length=255, required=False)
        synCookieEnable = serializers.CharField(max_length=255, required=False)
        synCookieWhitelist = serializers.CharField(max_length=255, required=False)
        tcpCloseTimeout = serializers.CharField(max_length=255, required=False)
        tcpGenerateIsn = serializers.CharField(max_length=255, required=False)
        tcpHandshakeTimeout = serializers.CharField(max_length=255, required=False)
        tcpPvaWhentoOffload = serializers.CharField(max_length=255, required=False)
        tcpStripSack = serializers.CharField(max_length=255, required=False)
        tcpWscaleMode = serializers.CharField(max_length=255, required=False)
        tcpTimestampMode = serializers.CharField(max_length=255, required=False)
        timeoutRecovery = serializers.CharField(max_length=255, required=False)

    items = F5ProfilesItemsSerializer(many=True)
