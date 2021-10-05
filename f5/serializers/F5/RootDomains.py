from rest_framework import serializers


class F5RootDomainsSerializer(serializers.Serializer):
    class F5RootDomainsInnerSerializer(serializers.Serializer):
        class F5RootDomainsItemsSerializer(serializers.Serializer):
            class F5RootDomainsValidatorsSerializer(serializers.Serializer):
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
                child=serializers.CharField(max_length=255, required=True)
            )
            vlansReference = F5RootDomainsValidatorsSerializer(many=True)

        items = F5RootDomainsItemsSerializer(many=True)

    data = F5RootDomainsInnerSerializer(required=True)
