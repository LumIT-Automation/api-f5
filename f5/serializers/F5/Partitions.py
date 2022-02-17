from rest_framework import serializers


class F5PartitionsSerializer(serializers.Serializer):
    class F5PartitionsItemsSerializer(serializers.Serializer):
        assetId = serializers.IntegerField(required=False)
        name = serializers.CharField(max_length=255, required=True)
        fullPath = serializers.CharField(max_length=255, required=False)
        generation = serializers.IntegerField(required=False)
        selfLink = serializers.CharField(max_length=255, required=False)
        defaultRouteDomain = serializers.IntegerField(required=False)

    items = F5PartitionsItemsSerializer(many=True)
