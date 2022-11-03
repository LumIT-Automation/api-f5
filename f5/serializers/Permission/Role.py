from rest_framework import serializers


class RoleSerializer(serializers.Serializer):
    role = serializers.CharField(max_length=64, required=True)
    description = serializers.CharField(max_length=255, required=True)
    privileges = serializers.ListField(
        child=serializers.CharField(max_length=64), required=False
    )
