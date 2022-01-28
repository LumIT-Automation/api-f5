from rest_framework import serializers


class F5PoolSerializer(serializers.Serializer):
    class F5PoolItemsMembersReferenceSerializer(serializers.Serializer):
        link = serializers.CharField(max_length=255, required=True)
        isSubcollection = serializers.BooleanField(required=True)

    name = serializers.CharField(max_length=255, required=True)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=255, required=False)
    allowNat = serializers.CharField(max_length=255, required=False)
    allowSnat = serializers.CharField(max_length=255, required=False)
    ignorePersistedWeight = serializers.CharField(max_length=255, required=False)
    ipTosToClient = serializers.CharField(max_length=255, required=False)
    ipTosToServer = serializers.CharField(max_length=255, required=False)
    linkQosToClient = serializers.CharField(max_length=255, required=False)
    linkQosToServer = serializers.CharField(max_length=255, required=False)
    loadBalancingMode = serializers.CharField(max_length=255, required=False)
    minActiveMembers = serializers.IntegerField(required=False)
    minUpMembers = serializers.IntegerField(required=False)
    minUpMembersAction = serializers.CharField(max_length=255, required=False)
    minUpMembersChecking = serializers.CharField(max_length=255, required=False)
    monitor = serializers.CharField(max_length=255, required=False)
    queueDepthLimit = serializers.IntegerField(required=False)
    queueOnConnectionLimit = serializers.CharField(max_length=255, required=False)
    queueTimeLimit = serializers.IntegerField(required=False)
    reselectTries = serializers.IntegerField(required=False)
    serviceDownAction = serializers.CharField(max_length=255, required=False)
    slowRampTime = serializers.IntegerField(required=False)
    membersReference = F5PoolItemsMembersReferenceSerializer(required=False)
