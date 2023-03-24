from rest_framework import serializers


class ConfigurationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    config_type = serializers.CharField(max_length=64, required=False)
    configuration = serializers.JSONField(required=True)
