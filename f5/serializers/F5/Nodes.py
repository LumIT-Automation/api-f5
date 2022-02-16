from rest_framework import serializers


class F5NodesSerializer(serializers.Serializer):
    class F5NodesItemsSerializer(serializers.Serializer):
        class F5NodesItemsFQDNSerializer(serializers.Serializer):
            addressFamily = serializers.CharField(max_length=255, required=True)
            autopopulate = serializers.CharField(max_length=255, required=True)
            interval = serializers.CharField(max_length=255, required=True)
            downInterval = serializers.IntegerField(required=True)

        assetId = serializers.IntegerField(required=True)
        name = serializers.CharField(max_length=255, required=True)
        partition = serializers.CharField(max_length=255, required=True)
        fullPath = serializers.CharField(max_length=255, required=True)
        generation = serializers.IntegerField(required=True)
        selfLink = serializers.CharField(max_length=255, required=True)
        address = serializers.IPAddressField(required=True)
        connectionLimit = serializers.IntegerField(required=True)
        dynamicRatio = serializers.IntegerField(required=True)
        ephemeral = serializers.CharField(max_length=255, required=True)
        fqdn = F5NodesItemsFQDNSerializer(required=True)
        logging = serializers.CharField(max_length=255, required=True)
        monitor = serializers.CharField(max_length=255, required=True)
        rateLimit = serializers.CharField(max_length=255, required=True)
        ratio = serializers.IntegerField(required=True)
        session = serializers.CharField(max_length=255, required=True)
        state = serializers.CharField(max_length=255, required=True)

    items = F5NodesItemsSerializer(many=True)
