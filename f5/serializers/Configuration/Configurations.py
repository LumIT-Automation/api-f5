from rest_framework import serializers
from f5.serializers.Configuration.Configuration import ConfigurationSerializer


class ConfigurationsSerializer(serializers.Serializer):
    items = ConfigurationSerializer(many=True, required=False)
