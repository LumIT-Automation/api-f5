from rest_framework import serializers

from f5.serializers.Permission.PermissionWorkflow import PermissionWorkflowSerializer


class PermissionsWorkflowSerializer(serializers.Serializer):
    items = PermissionWorkflowSerializer(many=True)
