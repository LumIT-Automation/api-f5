from rest_framework import serializers


class F5PoolMembersSerializer(serializers.Serializer):
    class F5PoolMembersItemsSerializer(serializers.Serializer):
        class F5PoolMembersInnerSerializer(serializers.Serializer):
            autopopulate = serializers.CharField(max_length=255, required=True)

        assetId = serializers.IntegerField(required=True)
        name = serializers.CharField(max_length=255, required=True)
        fullPath = serializers.CharField(max_length=255, required=True)
        generation = serializers.IntegerField(required=True)
        selfLink = serializers.CharField(max_length=255, required=True)
        address = serializers.CharField(max_length=255, required=True)
        connectionLimit = serializers.IntegerField(required=True)
        dynamicRatio = serializers.IntegerField(required=True)
        ephemeral = serializers.CharField(max_length=255, required=True)
        inheritProfile = serializers.CharField(max_length=255, required=True)
        logging = serializers.CharField(max_length=255, required=True)
        monitor = serializers.CharField(max_length=255, required=True)
        priorityGroup = serializers.IntegerField(required=True)
        rateLimit = serializers.CharField(max_length=255, required=True)
        ratio = serializers.IntegerField(required=True)
        session = serializers.CharField(max_length=255, required=True)
        state = serializers.CharField(max_length=255, required=True)
        fqdn = F5PoolMembersInnerSerializer(required=True)

    items = F5PoolMembersItemsSerializer(many=True)
