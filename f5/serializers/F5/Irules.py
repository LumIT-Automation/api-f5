from rest_framework import serializers


class F5IrulesSerializer(serializers.Serializer):
    class F5IrulesInnerSerializer(serializers.Serializer):
        class F5IrulesItemsSerializer(serializers.Serializer):
            name = serializers.CharField(max_length=255, required=True)
            partition = serializers.CharField(max_length=255, required=True)
            fullPath = serializers.CharField(max_length=255, required=True)
            generation = serializers.IntegerField(required=False)
            selfLink = serializers.CharField(max_length=255, required=True)
            apiAnonymous = serializers.CharField(required=True)

        items = F5IrulesItemsSerializer(many=True)

    data = F5IrulesInnerSerializer(required=True)