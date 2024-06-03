from rest_framework import serializers


class F5DatagroupSerializer(serializers.Serializer):
    class F5DatagroupRecordsSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=False)
        data = serializers.CharField(max_length=255, required=False)

    assetId = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=True)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    subPath = serializers.CharField(max_length=255, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=255, required=False)
    type = serializers.CharField(max_length=255, required=False)
    records = F5DatagroupRecordsSerializer(required=False, many=True)
