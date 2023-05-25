from rest_framework import serializers


class PrivilegeSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    privilege = serializers.CharField(max_length=255, required=True)
    privilege_type = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(max_length=255, required=True, allow_blank=True)
