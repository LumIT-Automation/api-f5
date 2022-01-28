from rest_framework import serializers


class F5PartitionsSerializer(serializers.Serializer):
    class F5PartitionsItemsSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=True)
        fullPath = serializers.CharField(max_length=255, required=True)
        generation = serializers.IntegerField(required=True)
        selfLink = serializers.CharField(max_length=255, required=True)
        defaultRouteDomain = serializers.IntegerField(required=True)

    items = F5PartitionsItemsSerializer(many=True)
