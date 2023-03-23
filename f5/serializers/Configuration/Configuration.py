from rest_framework import serializers


class ConfigurationSerializer(serializers.Serializer):
    configuration = serializers.JSONField(required=True)
