from rest_framework import serializers


class F5PoliciesSerializer(serializers.Serializer):
    class F5PoliciesItemsSerializer(serializers.Serializer):
        class F5PoliciesReferenceSerializer(serializers.Serializer):
            link = serializers.CharField(max_length=255, required=True)
            isSubcollection = serializers.BooleanField(required=False)

        name = serializers.CharField(max_length=255, required=True)
        partition = serializers.CharField(max_length=255, required=True)
        fullPath = serializers.CharField(max_length=255, required=True)
        subPath = serializers.CharField(max_length=255, required=False)
        generation = serializers.IntegerField(required=False)
        selfLink = serializers.CharField(max_length=255, required=True)
        lastModified = serializers.CharField(max_length=255, required=True)
        status = serializers.CharField(max_length=255, required=True)
        strategy = serializers.CharField(max_length=255, required=True)
        strategyReference = F5PoliciesReferenceSerializer(required=False)
        rulesReference = F5PoliciesReferenceSerializer(required=False)

    items = F5PoliciesItemsSerializer(many=True)
