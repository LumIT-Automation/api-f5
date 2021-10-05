from rest_framework import serializers


class ConfigurationSerializer(serializers.Serializer):
    class ConfigurationInnerSerializer(serializers.Serializer):
        configuration = serializers.CharField(max_length=255, required=True)

    data = ConfigurationInnerSerializer(required=True)
