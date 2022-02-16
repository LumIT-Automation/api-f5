from rest_framework import serializers


class F5PoolMemberSerializer(serializers.Serializer):
    class F5PoolMemberInnerFQDNSerializer(serializers.Serializer):
        autopopulate = serializers.CharField(max_length=255, required=True)

    assetId = serializers.IntegerField(required=True)
    name = serializers.CharField(max_length=255, required=True)
    connectionLimit =serializers.IntegerField(required=False)
    dynamicRatio =serializers.IntegerField(required=False)
    ephemeral = serializers.CharField(max_length=255, required=False)
    logging = serializers.CharField(max_length=255, required=False)
    monitor = serializers.CharField(max_length=255, required=False)
    priorityGroup = serializers.IntegerField(required=False)
    rateLimit = serializers.CharField(max_length=255, required=False)
    ratio = serializers.IntegerField(required=False)
    session = serializers.CharField(max_length=255, required=False)
    state = serializers.CharField(max_length=255, required=False) # do not modify.
    fqdn = F5PoolMemberInnerFQDNSerializer(required=True)
