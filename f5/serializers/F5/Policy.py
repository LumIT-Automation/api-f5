from rest_framework import serializers


class F5PolicySerializer(serializers.Serializer):
    class F5PolicyReferenceSerializer(serializers.Serializer):
        link = serializers.CharField(max_length=255, required=False)
        isSubcollection = serializers.BooleanField(required=False)

    assetId = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=True)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    subPath = serializers.CharField(max_length=255, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=255, required=False)
    status = serializers.CharField(max_length=255, required=False)
    lastModified = serializers.CharField(max_length=255, required=False)
    strategy = serializers.CharField(max_length=255, required=False)
    strategyReference = F5PolicyReferenceSerializer(required=False)
    rulesReference = F5PolicyReferenceSerializer(required=False)
