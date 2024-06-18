from rest_framework import serializers

from f5.serializers.Permission.Privilege import PrivilegeSerializer


class WorkflowSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    workflow = serializers.CharField(max_length=64, required=True)
    description = serializers.CharField(max_length=255, required=True, allow_blank=True)
    privileges = PrivilegeSerializer(many=True, required=False)
