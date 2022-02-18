from rest_framework import serializers


class F5NodeSerializer(serializers.Serializer):
    class F5NodesItemFQDNSerializer(serializers.Serializer):
        addressFamily = serializers.CharField(max_length=255, required=False)
        autopopulate = serializers.CharField(max_length=255, required=False)
        interval = serializers.CharField(max_length=255, required=False)
        downInterval = serializers.IntegerField(required=False)

    assetId = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=True)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=255, required=False)
    address = serializers.RegexField(regex='^([01]?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:[01]?\d\d?|2[0-4]\d|25[0-5])){3}(%\d)?$', required=True)
    connectionLimit = serializers.IntegerField(required=False)
    dynamicRatio = serializers.IntegerField(required=False)
    ephemeral = serializers.CharField(max_length=255, required=False)
    fqdn = F5NodesItemFQDNSerializer(required=False)
    logging = serializers.CharField(max_length=255, required=False)
    monitor = serializers.CharField(max_length=255, required=False)
    rateLimit = serializers.CharField(max_length=255, required=False)
    ratio = serializers.IntegerField(required=False)
    session = serializers.CharField(max_length=255, required=False)
    state = serializers.CharField(max_length=255, required=False)
