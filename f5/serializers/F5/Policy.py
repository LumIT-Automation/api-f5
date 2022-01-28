from rest_framework import serializers


class F5PolicySerializer(serializers.Serializer):
    class F5PolicyReferenceSerializer(serializers.Serializer):
        link = serializers.CharField(max_length=255, required=True)
        isSubcollection = serializers.BooleanField(required=False)

    name = serializers.CharField(max_length=255, required=True)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=255, required=False)
    status = serializers.CharField(max_length=255, required=False)
    strategy = serializers.CharField(max_length=255, required=False)
    strategyReference = F5PolicyReferenceSerializer(required=False)
    rulesReference = F5PolicyReferenceSerializer(required=False)
