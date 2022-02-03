from rest_framework import serializers


class ConfigurationSerializer(serializers.Serializer):
    configuration = serializers.CharField(max_length=255, required=True)
