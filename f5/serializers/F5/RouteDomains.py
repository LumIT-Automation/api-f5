from rest_framework import serializers


class F5RouteDomainsSerializer(serializers.Serializer):
    class F5RouteDomainsInnerSerializer(serializers.Serializer):
        class F5RouteDomainsItemsSerializer(serializers.Serializer):
            class F5RouteDomainsValidatorsSerializer(serializers.Serializer):
                link = serializers.CharField(max_length=255, required=True)

            name = serializers.CharField(max_length=255, required=True)
            partition = serializers.CharField(max_length=255, required=True)
            fullPath = serializers.CharField(max_length=255, required=True)
            generation = serializers.IntegerField(required=True)
            id = serializers.IntegerField(required=True)
            connectionLimit = serializers.IntegerField(required=True)
            selfLink = serializers.CharField(max_length=255, required=True)
            strict = serializers.CharField(max_length=255, required=True)
            throughputCapacity = serializers.CharField(max_length=255, required=True)
            defaultRouteDomain = serializers.IntegerField(required=False)
            vlans = serializers.ListField(
                child=serializers.CharField(max_length=255),
                required=False
            )
            vlansReference = F5RouteDomainsValidatorsSerializer(many=True, required=False)

        items = F5RouteDomainsItemsSerializer(many=True)

    data = F5RouteDomainsInnerSerializer(required=True)
