from rest_framework import serializers


class F5RouteDomainsSerializer(serializers.Serializer):
    class F5RouteDomainsItemsSerializer(serializers.Serializer):
        class F5RouteDomainsValidatorsSerializer(serializers.Serializer):
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
        throughputCapacity = serializers.CharField(max_length=255, required=False)
        defaultRouteDomain = serializers.IntegerField(required=False)
        vlans = serializers.ListField(
            child=serializers.CharField(max_length=255),
            required=False
        )
        vlansReference = F5RouteDomainsValidatorsSerializer(many=True, required=False)

    items = F5RouteDomainsItemsSerializer(many=True)
