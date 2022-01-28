from rest_framework import serializers


class F5IrulesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    apiAnonymous = serializers.CharField(required=False)
