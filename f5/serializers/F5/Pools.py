from rest_framework import serializers


class F5PoolsSerializer(serializers.Serializer):
    class F5PoolsItemsSerializer(serializers.Serializer):
        class F5PoolsItemsMembersReferenceSerializer(serializers.Serializer):
            link = serializers.CharField(max_length=255, required=True)
            isSubcollection = serializers.BooleanField(required=True)

        name = serializers.CharField(max_length=255, required=True)
        partition = serializers.CharField(max_length=255, required=True)
        fullPath = serializers.CharField(max_length=255, required=True)
        generation = serializers.IntegerField(required=True)
        selfLink = serializers.CharField(max_length=255, required=True)
        allowNat = serializers.CharField(max_length=255, required=True)
        allowSnat = serializers.CharField(max_length=255, required=True)
        ignorePersistedWeight = serializers.CharField(max_length=255, required=True)
        ipTosToClient = serializers.CharField(max_length=255, required=True)
        ipTosToServer = serializers.CharField(max_length=255, required=True)
        linkQosToClient = serializers.CharField(max_length=255, required=True)
        linkQosToServer = serializers.CharField(max_length=255, required=True)
        loadBalancingMode = serializers.CharField(max_length=255, required=True)
        minActiveMembers = serializers.IntegerField(required=True)
        minUpMembers = serializers.IntegerField(required=True)
        minUpMembersAction = serializers.CharField(max_length=255, required=True)
        minUpMembersChecking = serializers.CharField(max_length=255, required=True)
        monitor = serializers.CharField(max_length=255, required=False)
        queueDepthLimit = serializers.IntegerField(required=True)
        queueOnConnectionLimit = serializers.CharField(max_length=255, required=True)
        queueTimeLimit = serializers.IntegerField(required=True)
        reselectTries = serializers.IntegerField(required=True)
        serviceDownAction = serializers.CharField(max_length=255, required=True)
        slowRampTime = serializers.IntegerField(required=True)
        membersReference = F5PoolsItemsMembersReferenceSerializer(required=False)

    items = F5PoolsItemsSerializer(many=True)
